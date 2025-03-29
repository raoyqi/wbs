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

async def process_app_records(app_records, start_time):
    
    app_record_len = len(app_records)

    semaphore = asyncio.Semaphore(10)  # 限制并发的翻译请求数量

    async def translate_tag(tag_text, target_language="zh-CN"):
        async with semaphore:

            return await translate_with_cache(tag_text, target_language)

    def create_font_tag(content, lang="zh-CN"):
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

    for index, app_record in enumerate(app_records, start=1):
        end_time = time.time() - start_time
        print(f"\r正在处理第 {index} 个 app-record,预计还要花费{(end_time/index*(app_record_len-index))/60:.2f} 分钟", end='', flush=True)

        title_tag = app_record.find('app-summary-title')
        if title_tag:
            title_a_tag = title_tag.find('a')
            if title_a_tag:
                
                title_a_text = title_a_tag.get_text(strip=True)
                title_mark_texts = [mark.get_text() for mark in title_a_tag.find_all('mark')]

                title_a_tag['data-immersive-translate-paragraph'] = '1'
                title_a_tag['data-immersive-translate-walked'] = '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'

                # 获取翻译后的标题
                translated_title = await translate_tag(title_a_text)
                font_tag = create_font_tag(translated_title)
                title_a_tag.append(font_tag)

                # 翻译标题中的标记文本
                for title_mark_word in title_mark_texts:
                    translated_mark_word = await translate_tag(title_mark_word)
                    mark_tag = soup.new_tag('mark', **{
                        'data-immersive-translate-walked': '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'
                    })
                    mark_tag.string = translated_mark_word
                    font_tag.append(mark_tag)

        app_jcr_sidenav = app_record.find('app-jcr-sidenav')
        
        if app_jcr_sidenav:
            journey_span = next(
                (span for span in app_jcr_sidenav.find_all('span') if isinstance(span, Tag) and not span.has_attr('class') and not span.has_attr('style')),
                None
            )
            if journey_span:
                journey_span_text = journey_span.get_text()
                translated_journey = await translate_tag(journey_span_text)

                font_tag = create_font_tag(translated_journey)
                journey_span.append(font_tag)

        for conf_span in app_record.find_all('span', attrs={'name': 'conf_title'}):
            conf_text = conf_span.get_text()
            translated_conf = await translate_tag(conf_text)
            font_tag = create_font_tag(translated_conf)
            conf_span.insert_after(font_tag)

        for second_conf_span in app_record.find_all('span', class_='summary-source-title noLink ng-star-inserted'):
            second_conf_text = second_conf_span.get_text()
            translated_second_conf = await translate_tag(second_conf_text)
            font_tag = create_font_tag(translated_second_conf)
            second_conf_span.insert_after(font_tag)

        for first_content_span in app_record.find_all('span', attrs={'cdxanalyticsaction': 'Search', 'id': True, 'cdxanalyticscategory': True, 'lang': True}):
            if first_content_span:

                parent = first_content_span.find_parent()

                grandparent = parent.find_parent() if parent else None

                if grandparent:

                    if 'style' in grandparent.attrs:

                        grandparent['style'] += ' height:auto!important'
                    else:

                        grandparent['style'] = 'height:auto!important'
                        
            content_p_tag = first_content_span.find('p')
            
            if content_p_tag:
                content_text = content_p_tag.get_text()
                translated_content = await translate_tag(content_text)

                font_tag = create_font_tag(translated_content)
                content_p_tag.append(font_tag)

                first_content_span['style'] = 'max-height:50px'
                first_content_span['data-immersive-translate-walked'] = '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'


def sort_files_by_number(files):

    return sorted(files, key=lambda x: [int(i) if i.isdigit() else i.lower() for i in re.split('(\d+)', x)])

if __name__ == "__main__":
    
    input_folder = "test_webofsci"
    output_folder = "translate"

    all_files = os.listdir(input_folder)
    html_files = [file for file in all_files if file.endswith('.html')]

    sorted_html_files = sort_files_by_number(html_files)

    for file_name in sorted_html_files:
        
        input_file_path = os.path.join(input_folder, file_name)
        
        
        output_file_name, _ = os.path.splitext(os.path.basename(input_file_path))

        output_file_path = os.path.join(output_folder, f"{output_file_name}_translate.html")

        # 确保目标文件夹存在
        os.makedirs(output_folder, exist_ok=True)
        print(output_file_path)
        if os.path.exists(output_file_path):
            print(f"文件 {output_file_path} 已存在，跳过处理。")
            continue
        print(f"正在处理文件 {output_file_path} ")

        with open(input_file_path, 'r', encoding='utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'lxml')

        app_records = soup.find_all('app-record')
        
        start_time = time.time()

        asyncio.run(process_app_records(app_records, start_time))

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



        # 保存修改后的 HTML
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(modified_html)

        print(f"HTML 已保存为 {output_file_path}")

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"执行时间: {execution_time:.4f} 秒")
