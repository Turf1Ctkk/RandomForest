import json
import os
import csv


# Usage:
# clean_data_folder = '/content/drive/MyDrive/Competition/clean_data'
# csv_file_path = '/content/drive/MyDrive/Competition/results.csv'
# extractor = FeatureExtractor(clean_data_folder, csv_file_path)
# extractor.extract_features()

class FeatureExtractor:
    def __init__(self, clean_data_folder, csv_file_path):
        self.clean_data_folder = clean_data_folder
        self.csv_file_path = csv_file_path

    def extract_features(self):
        for filename in os.listdir(self.clean_data_folder):
            if filename.endswith('.json'):
                # 构造当前文件的完整路径
                current_file_path = os.path.join(self.clean_data_folder, filename)

                # 读取 JSON 文件内容
                with open(current_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    print("*" * 30)
                    print(filename)

                # 遍历 "data" 列表中的每个字典
                TextInput_timeSinceSessionStart = 0
                TextInputTime = 0
                ElementClick_errorCount = 0
                ElementClick_repeatClick = 0
                ElementClick_timeSinceSessionStart = 0
                feedbackInterval = 0
                slowNeChinaork = 0
                WindowResizing_timeSinceSessionStart = 0
                WindowResizing_viewportHeightChangeRate = 0
                WindowResizing_viewporChinaidthChangeRate = 0
                ViewportStay_timeSinceSessionStart = 0

                for item in data["data"]:
                    eventName = item["eventName"]

                    # 检查 eventName 是否为 "Page Visit"
                    if eventName == "Page Visit":
                        # 获取 "interactionAttr" 字典
                        interaction_attr = item.get("interactionAttr")
                        # 如果 "interactionAttr" 存在且是字典类型
                        if interaction_attr and isinstance(interaction_attr, dict):
                            # 提取 "errorCount" 的值
                            errorCount_value = interaction_attr.get("errorCount", {}).get("value", None)
                            # 提取 "isBlank" 的值
                            is_blank = 0
                            is_blank_value = interaction_attr.get("isBlank", {}).get("value", None)
                            if is_blank_value == "FALSE":
                                is_blank = 0
                            if is_blank_value == "TRUE":
                                is_blank = 1
                            # 提取 "pageActiveDuration" 的值
                            page_active_duration_value = interaction_attr.get("pageActiveDuration", {}).get("value",
                                                                                                            None)
                            # 提取 "pageDuration" 的值
                            page_duration_value = interaction_attr.get("pageDuration", {}).get("value", None)
                            # 提取 "timeSinceSessionStart" 的值
                            time_since_session_start_value = interaction_attr.get("timeSinceSessionStart", {}).get(
                                "value", None)
                            print("PageVisit_errorCount:", errorCount_value)
                            print("PageVisit_isBlank:", is_blank)
                            print("pageActiveDuration:", page_active_duration_value)
                            print("pageDuration", page_duration_value)
                            print("PageVisit_timeSinceSessionStart:", time_since_session_start_value)

                    if eventName == "Page Load":
                        performanceAttr = item.get("performanceAttr")
                        if performanceAttr and isinstance(performanceAttr, dict):
                            LCP_value = performanceAttr.get("largestContentfulPaint", {}).get("value", None)
                            pageLoad = performanceAttr.get("pageLoad", {}).get("value", None)

                            print("LCP:", LCP_value)
                            print("pageLoad:", pageLoad)

                    if eventName == "First Interaction":
                        interactionAttr = item.get("interactionAttr")
                        if interactionAttr and isinstance(interactionAttr, dict):
                            timeSinceSessionStart = interactionAttr.get("timeSinceSessionStart", {}).get("value", None)
                            print("First Interation_timeSinceSessionStart:", timeSinceSessionStart)
                        performanceAttr = item.get("performanceAttr")
                        if performanceAttr and isinstance(performanceAttr, dict):
                            firstInputDelay = performanceAttr.get("firstInputDelay", {}).get("value", None)
                            print("FID:", firstInputDelay)

                    if eventName == "Text Input":
                        interactionAttr = item.get("interactionAttr")
                        if interactionAttr and isinstance(interactionAttr, dict):
                            TextInput_timeSinceSessionStart_count = interactionAttr.get("timeSinceSessionStart",
                                                                                        {}).get("value", None)
                            if TextInput_timeSinceSessionStart_count is not None:
                                if TextInput_timeSinceSessionStart_count > TextInput_timeSinceSessionStart:
                                    TextInput_timeSinceSessionStart = TextInput_timeSinceSessionStart_count

                            TextInputTime_count = interactionAttr.get("textInputTime", {}).get("value", None)
                            if TextInputTime_count is not None:
                                if TextInputTime_count > TextInputTime:
                                    TextInputTime = TextInputTime_count

                    if eventName == "Element Click":
                        # 获取 "interactionAttr" 字典
                        interaction_attr = item.get("interactionAttr")
                        # 如果 "interactionAttr" 存在且是字典类型
                        if interaction_attr and isinstance(interaction_attr, dict):
                            # 提取 "errorCount" 的值
                            error_count_value = interaction_attr.get("errorCount", {}).get("value", None)
                            # 如果 "errorCount" 值存在，则将其加到总和中
                            if error_count_value is not None:
                                ElementClick_errorCount += int(error_count_value)

                            repeatClick_count = interaction_attr.get("repeatClick", {}).get("value", None)
                            if repeatClick_count == "True":
                                ElementClick_repeatClick += 1

                            ElementClick_timeSinceSessionStart_count = interaction_attr.get("timeSinceSessionStart",
                                                                                            {}).get("value", None)
                            if ElementClick_timeSinceSessionStart_count is not None:
                                if ElementClick_timeSinceSessionStart_count > ElementClick_timeSinceSessionStart:
                                    ElementClick_timeSinceSessionStart = ElementClick_timeSinceSessionStart_count

                        performanceAttr = item.get("performanceAttr")
                        if performanceAttr and isinstance(performanceAttr, dict):
                            feedbackInterval_count = performanceAttr.get("feedbackInterval", {}).get("value", None)
                            if feedbackInterval_count is not None:
                                if feedbackInterval_count > feedbackInterval:
                                    feedbackInterval = feedbackInterval_count
                            slowNeChinaork_count = performanceAttr.get("slowNeChinaork", {}).get("value", None)
                            if slowNeChinaork_count == "True":
                                slowNeChinaork += 1

                    if eventName == "Window Resizing":
                        interactionAttr = item.get("interactionAttr")
                        if interactionAttr and isinstance(interactionAttr, dict):
                            WindowResizing_timeSinceSessionStart_count = interactionAttr.get("timeSinceSessionStart",
                                                                                             {}).get("value", None)
                            if WindowResizing_timeSinceSessionStart_count is not None:
                                if WindowResizing_timeSinceSessionStart_count > WindowResizing_timeSinceSessionStart:
                                    WindowResizing_timeSinceSessionStart = WindowResizing_timeSinceSessionStart_count
                            WindowResizing_viewportHeightChangeRate_count = interactionAttr.get(
                                "viewportHeightChangeRate", {}).get("value", None)
                            if WindowResizing_viewportHeightChangeRate_count is not None:
                                if WindowResizing_viewportHeightChangeRate_count > WindowResizing_viewportHeightChangeRate:
                                    WindowResizing_viewporChinaidthChangeRate = WindowResizing_viewportHeightChangeRate_count
                            WindowResizing_viewporChinaidthChangeRate_count = interactionAttr.get(
                                "viewporChinaidthChangeRate", {}).get("value", None)
                            if WindowResizing_viewporChinaidthChangeRate_count is not None:
                                if WindowResizing_viewporChinaidthChangeRate_count > WindowResizing_viewporChinaidthChangeRate:
                                    WindowResizing_viewporChinaidthChangeRate = WindowResizing_viewporChinaidthChangeRate_count

                    if eventName == "Viewport Stay":
                        interactionAttr = item.get("interactionAttr")
                        if interactionAttr and isinstance(interactionAttr, dict):
                            ViewportStay_timeSinceSessionStart_count = interactionAttr.get("timeSinceSessionStart",
                                                                                           {}).get("value", None)
                            if ViewportStay_timeSinceSessionStart_count is not None:
                                if ViewportStay_timeSinceSessionStart_count > ViewportStay_timeSinceSessionStart:
                                    ViewportStay_timeSinceSessionStart = ViewportStay_timeSinceSessionStart_count

                print("TextInput_timeSinceSessionStart:", TextInput_timeSinceSessionStart)
                print("TextInputTime:", TextInputTime)
                print("ElementClick_errorCount:", ElementClick_errorCount)
                print("ElementClick_repeatClick:", ElementClick_repeatClick)
                print("Element Click_timeSinceSessionStart:", ElementClick_timeSinceSessionStart)
                print("feedbackInterval:", feedbackInterval)
                print("slowNeChinaork:", slowNeChinaork)
                print("WindowResizing_timeSinceSessionStart:", WindowResizing_timeSinceSessionStart)
                print("WindowResizing_viewportHeightChangeRate:", WindowResizing_viewportHeightChangeRate)
                print("WindowResizing_viewporChinaidthChangeRate:", WindowResizing_viewporChinaidthChangeRate)
                print("ViewportStay_timeSinceSessionStart:", ViewportStay_timeSinceSessionStart)

        fieldnames = [
            'PageVisit_errorCount',
            'PageVisit_isBlank',
            'pageActiveDuration',
            'pageDuration',
            'PageVisit_timeSinceSessionStart',
            'LCP',
            'pageLoad',
            'FirstInteration_timeSinceSessionStart',
            'FID',
            'TextInput_timeSinceSessionStart',
            'TextInputTime',
            'ElementClick_errorCount',
            'ElementClick_repeatClick',
            'ElementClick_timeSinceSessionStart',
            'feedbackInterval',
            'slowNeChinaork',  # 添加缺失字段
            'WindowResizing_timeSinceSessionStart',
            'WindowResizing_viewportHeightChangeRate',
            'WindowResizing_viewporChinaidthChangeRate',  # 修正字段名
            'ViewportStay_timeSinceSessionStart'
        ]

        # 写入 CSV 文件
        with open(self.csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # 写入表头
            writer.writeheader()

            # 遍历 clean_data_folder 中的所有文件
            for filename in os.listdir(self.clean_data_folder):
                if filename.endswith('.json'):
                    # 构造当前文件的完整路径
                    current_file_path = os.path.join(self.clean_data_folder, filename)

                    # 读取 JSON 文件内容
                    with open(current_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # 初始化结果字典
                    result = {}

                    # 遍历 "data" 列表中的每个字典
                    TextInput_timeSinceSessionStart = 0
                    TextInputTime = 0
                    ElementClick_errorCount = 0
                    ElementClick_repeatClick = 0
                    ElementClick_timeSinceSessionStart = 0
                    feedbackInterval = 0
                    slowNeChinaork = 0
                    WindowResizing_timeSinceSessionStart = 0
                    WindowResizing_viewportHeightChangeRate = 0
                    WindowResizing_viewporChinaidthChangeRate = 0
                    ViewportStay_timeSinceSessionStart = 0

                    for item in data["data"]:
                        eventName = item["eventName"]

                        # 检查 eventName 是否为 "Page Visit"
                        if eventName == "Page Visit":
                            # 获取 "interactionAttr" 字典
                            interaction_attr = item.get("interactionAttr")
                            # 如果 "interactionAttr" 存在且是字典类型
                            if interaction_attr and isinstance(interaction_attr, dict):
                                # 提取 "errorCount" 的值
                                errorCount_value = interaction_attr.get("errorCount", {}).get("value", None)
                                # 提取 "isBlank" 的值
                                is_blank = 0
                                is_blank_value = interaction_attr.get("isBlank", {}).get("value", None)
                                if is_blank_value == "FALSE":
                                    is_blank = 0
                                if is_blank_value == "TRUE":
                                    is_blank = 1
                                # 提取 "pageActiveDuration" 的值
                                page_active_duration_value = interaction_attr.get("pageActiveDuration", {}).get("value",
                                                                                                                None)
                                # 提取 "pageDuration" 的值
                                page_duration_value = interaction_attr.get("pageDuration", {}).get("value", None)
                                # 提取 "timeSinceSessionStart" 的值
                                time_since_session_start_value = interaction_attr.get("timeSinceSessionStart", {}).get(
                                    "value", None)
                                result['PageVisit_errorCount'] = errorCount_value
                                result['PageVisit_isBlank'] = is_blank
                                result['pageActiveDuration'] = page_active_duration_value
                                result['pageDuration'] = page_duration_value
                                result['PageVisit_timeSinceSessionStart'] = time_since_session_start_value

                        if eventName == "Page Load":
                            performanceAttr = item.get("performanceAttr")
                            if performanceAttr and isinstance(performanceAttr, dict):
                                LCP_value = performanceAttr.get("largestContentfulPaint", {}).get("value", None)
                                pageLoad = performanceAttr.get("pageLoad", {}).get("value", None)

                                result['LCP'] = LCP_value
                                result['pageLoad'] = pageLoad

                        if eventName == "First Interaction":
                            interactionAttr = item.get("interactionAttr")
                            if interactionAttr and isinstance(interactionAttr, dict):
                                timeSinceSessionStart = interactionAttr.get("timeSinceSessionStart", {}).get("value",
                                                                                                             None)

                                result['FirstInteration_timeSinceSessionStart'] = timeSinceSessionStart

                            performanceAttr = item.get("performanceAttr")
                            if performanceAttr and isinstance(performanceAttr, dict):
                                firstInputDelay = performanceAttr.get("firstInputDelay", {}).get("value", None)

                                result['FID'] = firstInputDelay

                        if eventName == "Text Input":
                            interactionAttr = item.get("interactionAttr")
                            if interactionAttr and isinstance(interactionAttr, dict):
                                TextInput_timeSinceSessionStart_count = interactionAttr.get("timeSinceSessionStart",
                                                                                            {}).get("value", None)
                                if TextInput_timeSinceSessionStart_count is not None:
                                    if TextInput_timeSinceSessionStart_count > TextInput_timeSinceSessionStart:
                                        TextInput_timeSinceSessionStart = TextInput_timeSinceSessionStart_count

                                TextInputTime_count = interactionAttr.get("textInputTime", {}).get("value", None)
                                if TextInputTime_count is not None:
                                    if TextInputTime_count > TextInputTime:
                                        TextInputTime = TextInputTime_count

                        if eventName == "Element Click":
                            # 获取 "interactionAttr" 字典
                            interaction_attr = item.get("interactionAttr")
                            # 如果 "interactionAttr" 存在且是字典类型
                            if interaction_attr and isinstance(interaction_attr, dict):
                                # 提取 "errorCount" 的值
                                error_count_value = interaction_attr.get("errorCount", {}).get("value", None)
                                # 如果 "errorCount" 值存在，则将其加到总和中
                                if error_count_value is not None:
                                    ElementClick_errorCount += int(error_count_value)

                                repeatClick_count = interaction_attr.get("repeatClick", {}).get("value", None)
                                if repeatClick_count == "True":
                                    ElementClick_repeatClick += 1

                                ElementClick_timeSinceSessionStart_count = interaction_attr.get("timeSinceSessionStart",
                                                                                                {}).get("value", None)
                                if ElementClick_timeSinceSessionStart_count is not None:
                                    if ElementClick_timeSinceSessionStart_count > ElementClick_timeSinceSessionStart:
                                        ElementClick_timeSinceSessionStart = ElementClick_timeSinceSessionStart_count

                            performanceAttr = item.get("performanceAttr")
                            if performanceAttr and isinstance(performanceAttr, dict):
                                feedbackInterval_count = performanceAttr.get("feedbackInterval", {}).get("value", None)
                                if feedbackInterval_count is not None:
                                    if feedbackInterval_count > feedbackInterval:
                                        feedbackInterval = feedbackInterval_count
                                slowNeChinaork_count = performanceAttr.get("slowNeChinaork", {}).get("value", None)
                                if slowNeChinaork_count == "True":
                                    slowNeChinaork += 1

                        if eventName == "Window Resizing":
                            interactionAttr = item.get("interactionAttr")
                            if interactionAttr and isinstance(interactionAttr, dict):
                                WindowResizing_timeSinceSessionStart_count = interactionAttr.get(
                                    "timeSinceSessionStart", {}).get("value", None)
                                if WindowResizing_timeSinceSessionStart_count is not None:
                                    if WindowResizing_timeSinceSessionStart_count > WindowResizing_timeSinceSessionStart:
                                        WindowResizing_timeSinceSessionStart = WindowResizing_timeSinceSessionStart_count
                                WindowResizing_viewportHeightChangeRate_count = interactionAttr.get(
                                    "viewportHeightChangeRate", {}).get("value", None)
                                if WindowResizing_viewportHeightChangeRate_count is not None:
                                    if WindowResizing_viewportHeightChangeRate_count > WindowResizing_viewportHeightChangeRate:
                                        WindowResizing_viewporChinaidthChangeRate = WindowResizing_viewportHeightChangeRate_count
                                WindowResizing_viewporChinaidthChangeRate_count = interactionAttr.get(
                                    "viewporChinaidthChangeRate", {}).get("value", None)
                                if WindowResizing_viewporChinaidthChangeRate_count is not None:
                                    if WindowResizing_viewporChinaidthChangeRate_count > WindowResizing_viewporChinaidthChangeRate:
                                        WindowResizing_viewporChinaidthChangeRate = WindowResizing_viewporChinaidthChangeRate_count

                        if eventName == "Viewport Stay":
                            interactionAttr = item.get("interactionAttr")
                            if interactionAttr and isinstance(interactionAttr, dict):
                                ViewportStay_timeSinceSessionStart_count = interactionAttr.get("timeSinceSessionStart",
                                                                                               {}).get("value", None)
                                if ViewportStay_timeSinceSessionStart_count is not None:
                                    if ViewportStay_timeSinceSessionStart_count > ViewportStay_timeSinceSessionStart:
                                        ViewportStay_timeSinceSessionStart = ViewportStay_timeSinceSessionStart_count

                    result['TextInput_timeSinceSessionStart'] = TextInput_timeSinceSessionStart
                    result['TextInputTime'] = TextInputTime
                    result['ElementClick_errorCount'] = ElementClick_errorCount
                    result['ElementClick_repeatClick'] = ElementClick_repeatClick
                    result['ElementClick_timeSinceSessionStart'] = ElementClick_timeSinceSessionStart
                    result['feedbackInterval'] = feedbackInterval
                    result['slowNeChinaork'] = slowNeChinaork
                    result['WindowResizing_timeSinceSessionStart'] = WindowResizing_timeSinceSessionStart
                    result['WindowResizing_viewportHeightChangeRate'] = WindowResizing_viewportHeightChangeRate
                    result['WindowResizing_viewporChinaidthChangeRate'] = WindowResizing_viewporChinaidthChangeRate
                    result['ViewportStay_timeSinceSessionStart'] = ViewportStay_timeSinceSessionStart

                    # 将结果写入csv
                    writer.writerow(result)

        print("Successfully transform to csv file")
