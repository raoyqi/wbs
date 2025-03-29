import asyncio
from bs4 import BeautifulSoup, Tag
import os
import re
import time
from translator import google_translate_long_text_async

translation_cache = {}

async def translate_with_cache(text, target_language="zh-CN"):
    if text not in translation_cache:
        translation_cache[text] = await google_translate_long_text_async(text, target_language)
    return translation_cache[text]

def create_font_tag(soup, content, lang="zh-CN"):
    font_tag = soup.new_tag('font', **{
        'class': 'notranslate immersive-translate-target-wrapper',
        'data-immersive-translate-translation-element-mark': '1',
        'lang': lang
    })
    font_inner_tag = soup.new_tag('font', **{
        'class': 'notranslate immersive-translate-target-inner immersive-translate-target-translation-theme-none-inner',
        'data-immersive-translate-translation-element-mark': '1'
    })
    font_inner_tag.string = content
    font_tag.append(font_inner_tag)
    return font_tag

async def process_app_records_batch(soup, app_records, start_time):
    text_blocks = []
    text_targets = []

    # === 1. 批量提取所有需要翻译的文本 ===
    for index, app_record in enumerate(app_records, start=1):
        end_time = time.time() - start_time
        print(f"\r正在提取第 {index}/{len(app_records)} 个 app-record, 预计还需 {(end_time/index*(len(app_records)-index))/60:.2f} 分钟", end='', flush=True)

        # title
        title_tag = app_record.find('app-summary-title')
        if title_tag:
            title_a_tag = title_tag.find('a')
            if title_a_tag:
                title_a_text = title_a_tag.get_text(strip=True)
                text_blocks.append(title_a_text)
                text_targets.append(('title', title_a_tag))

                for mark in title_a_tag.find_all('mark'):
                    mark_text = mark.get_text()
                    text_blocks.append(mark_text)
                    text_targets.append(('mark', mark))

        # sidenav
        app_jcr_sidenav = app_record.find('app-jcr-sidenav')
        if app_jcr_sidenav:
            journey_span = next(
                (span for span in app_jcr_sidenav.find_all('span') if isinstance(span, Tag) and not span.has_attr('class') and not span.has_attr('style')),
                None
            )
            if journey_span:
                journey_text = journey_span.get_text()
                text_blocks.append(journey_text)
                text_targets.append(('journey', journey_span))

        # conf
        for conf_span in app_record.find_all('span', attrs={'name': 'conf_title'}):
            conf_text = conf_span.get_text()
            text_blocks.append(conf_text)
            text_targets.append(('conf', conf_span))

        for second_conf_span in app_record.find_all('span', class_='summary-source-title noLink ng-star-inserted'):
            second_conf_text = second_conf_span.get_text()
            text_blocks.append(second_conf_text)
            text_targets.append(('second_conf', second_conf_span))

        for content_span in app_record.find_all('span', attrs={'cdxanalyticsaction': 'Search', 'id': True, 'cdxanalyticscategory': True, 'lang': True}):
            parent = content_span.find_parent()
            grandparent = parent.find_parent() if parent else None
            if grandparent:
                grandparent['style'] = grandparent.get('style', '') + ' height:auto!important'

            content_p_tag = content_span.find('p')
            if content_p_tag:
                content_text = content_p_tag.get_text()
                text_blocks.append(content_text)
                text_targets.append(('content', content_p_tag, content_span))

    # === 2. 批量翻译 ===
    print(f"\n开始翻译 {len(text_blocks)} 段文本...")
    batch_text = "\n".join(text_blocks)
    translated_batch = await translate_with_cache(batch_text, "zh-CN")
    translated_texts = translated_batch.split("\n")

    # === 3. 回填翻译结果 ===
    for info, translated in zip(text_targets, translated_texts):
        if info[0] == 'title':
            font_tag = create_font_tag(soup, translated)
            info[1].append(font_tag)
            info[1]['data-immersive-translate-paragraph'] = '1'
            info[1]['data-immersive-translate-walked'] = '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'
        elif info[0] == 'mark':
            mark_tag = soup.new_tag('mark', **{
                'data-immersive-translate-walked': '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'
            })
            mark_tag.string = translated
            info[1].insert_after(mark_tag)
        elif info[0] == 'journey':
            font_tag = create_font_tag(soup, translated)
            info[1].append(font_tag)
        elif info[0] in ('conf', 'second_conf'):
            font_tag = create_font_tag(soup, translated)
            info[1].insert_after(font_tag)
        elif info[0] == 'content':
            font_tag = create_font_tag(soup, translated)
            info[1].append(font_tag)
            info[2]['style'] = 'max-height:50px'
            info[2]['data-immersive-translate-walked'] = '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'

    print(f"\n✅ 已完成回填 {len(app_records)} 个 app-record")

def sort_files_by_number(files):
    return sorted(files, key=lambda x: [int(i) if i.isdigit() else i.lower() for i in re.split('(\d+)', x)])

if __name__ == "__main__":
    input_folder = "webofsci"
    output_folder = "translate"

    all_files = os.listdir(input_folder)
    html_files = [file for file in all_files if file.endswith('.html')]

    sorted_html_files = sort_files_by_number(html_files)

    for file_name in sorted_html_files:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_name, _ = os.path.splitext(os.path.basename(input_file_path))
        output_file_path = os.path.join(output_folder, f"{output_file_name}_translate.html")
        os.makedirs(output_folder, exist_ok=True)

        print(f"\n=== 正在处理文件：{output_file_path} ===")
        if os.path.exists(output_file_path):
            print(f"文件 {output_file_path} 已存在，跳过处理。")
            continue

        with open(input_file_path, 'r', encoding='utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'lxml')
        app_records = soup.find_all('app-record')

        start_time = time.time()
        asyncio.run(process_app_records_batch(soup, app_records, start_time))

        # 清理多余元素
        selectors_to_remove = [
            {'method': 'find_all', 'args': {'class_': '_pendo-step-container-size'}},
            {'method': 'select', 'args': {'selector': '[aria-label="Open Resource Center, 19 new notifications"]'}},
            {'method': 'select', 'args': {'selector': '[class="show-more show-more-text wos-new-primary-color"]'}}
        ]

        for selector in selectors_to_remove:
            method = getattr(soup, selector['method'])
            elements_to_remove = method(**selector['args'])
            for element in elements_to_remove:
                element.decompose()

        modified_html = soup.prettify()

        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(modified_html)

        print(f"✅ 已保存翻译文件：{output_file_path}")
        print(f"⏱️ 执行时间: {time.time() - start_time:.2f} 秒")
