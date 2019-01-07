from selenium import webdriver

# ————————打开网页
b = webdriver.Chrome()  # 打开浏览器
b.get('https://www.baidu.com')
title = b.title  # 获得网页title
print(title)
www = b.current_url  # 返回打开的网址
print(www)

# ————————定位元素
ele = b.find_element_by_id('kw')  # 根据id定位元素
ele = b.find_element_by_name('wd')  # 根据name定位元素

ele2 = b.find_element_by_tag_name('input')  # 根据标签名定位元素




# ———————常用操作
ele.clear()  # 清空
ele.send_keys('李小龙')  # 模拟键盘输入
ele.back()  # 返回上一级

b.maximize_window()  # 最大化窗口
b.close()  # 关闭当前窗口
b.quit()  # 关闭浏览器

# ———————如果需要定位的元素在frame内，需要先进入frame
b.switch_to_frame('ptlogin_iframe')  # 先定位到frame里面

# ———————遇到新标签窗口
now_handle = b.current_window_handle  # 先拿到原来窗口的句柄
print(now_handle)
all_handles = b.window_handles  # 拿到全部窗口的句柄
for handle in all_handles:  # 比对句柄
    print(handle)
    if handle != now_handle:
        b.switch_to_window(handle)  # 跳转到新窗口
b.close()  # 关闭当前窗口
b.quit()  # 关闭浏览器
