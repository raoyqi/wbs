async def process_app_records(app_records, start_time):
    # ... 省略原来的代码

    for index, app_record in enumerate(app_records, start=1):
        # ...打印进度条

        text_blocks = []  # 要翻译的所有文本
        text_targets = []  # 记录文本的插入位置及类型，后面拆回来时用

        # 收集标题
        title_tag = app_record.find('app-summary-title')
        if title_tag:
            title_a_tag = title_tag.find('a')
            if title_a_tag:
                title_a_text = title_a_tag.get_text(strip=True)
                text_blocks.append(title_a_text)
                text_targets.append(('title', title_a_tag))

                # mark 也收集
                for mark in title_a_tag.find_all('mark'):
                    mark_text = mark.get_text()
                    text_blocks.append(mark_text)
                    text_targets.append(('mark', mark))

        # 收集 sidenav
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

        # 收集 conf_title
        for conf_span in app_record.find_all('span', attrs={'name': 'conf_title'}):
            conf_text = conf_span.get_text()
            text_blocks.append(conf_text)
            text_targets.append(('conf', conf_span))

        # 收集 second_conf
        for second_conf_span in app_record.find_all('span', class_='summary-source-title noLink ng-star-inserted'):
            second_conf_text = second_conf_span.get_text()
            text_blocks.append(second_conf_text)
            text_targets.append(('second_conf', second_conf_span))

        # 收集正文内容
        for content_span in app_record.find_all('span', attrs={'cdxanalyticsaction': 'Search', 'id': True, 'cdxanalyticscategory': True, 'lang': True}):
            content_p_tag = content_span.find('p')
            if content_p_tag:
                content_text = content_p_tag.get_text()
                text_blocks.append(content_text)
                text_targets.append(('content', content_p_tag, content_span))

        # -------------------
        # **批量翻译**
        if text_blocks:
            batch_text = "\n".join(text_blocks)
            translated_batch = await translate_with_cache(batch_text, "zh-CN")
            translated_texts = translated_batch.split("\n")

            # 回填翻译结果
            for (info, translated) in zip(text_targets, translated_texts):
                if info[0] == 'title':
                    font_tag = create_font_tag(translated)
                    info[1].append(font_tag)
                    info[1]['data-immersive-translate-paragraph'] = '1'
                    info[1]['data-immersive-translate-walked'] = '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'
                elif info[0] == 'mark':
                    mark_tag = soup.new_tag('mark', **{
                        'data-immersive-translate-walked': '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'
                    })
                    mark_tag.string = translated
                    # 这里可以根据你需求附加到 font_tag
                elif info[0] == 'journey':
                    font_tag = create_font_tag(translated)
                    info[1].append(font_tag)
                elif info[0] in ('conf', 'second_conf'):
                    font_tag = create_font_tag(translated)
                    info[1].insert_after(font_tag)
                elif info[0] == 'content':
                    font_tag = create_font_tag(translated)
                    info[1].append(font_tag)
                    info[2]['style'] = 'max-height:50px'
                    info[2]['data-immersive-translate-walked'] = '6486b4bb-16ed-40ff-86fa-b7e1ab33e2a7'
