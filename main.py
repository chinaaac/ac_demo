from playwright.sync_api import sync_playwright
import sys
import time


def open_baidu_with_playwright():
    """使用 Playwright 打开百度（带页面加载验证）"""
    print("正在启动浏览器，打开百度...")

    try:
        # 启动 Playwright（使用 Chromium 浏览器，非无头模式）
        with sync_playwright() as p:
            # 启动浏览器（headless=False 显示浏览器窗口，slow_mo 放慢操作便于观察）
            browser = p.chromium.launch(
                headless=False,
                channel="chrome",
                slow_mo=500,  # 每个操作延迟 500ms
                args=["--start-maximized"]  # 浏览器最大化
            )

            # 创建新页面
            page = browser.new_page(
                viewport={"width": 1920, "height": 1080}  # 设置窗口大小
            )

            # 打开百度首页，等待页面加载完成（超时 10 秒）
            page.goto("https://www.baidu.com", timeout=10000)

            # 验证页面加载成功（等待百度搜索框出现）
            page.wait_for_selector("#kw", timeout=5000)  # 等待搜索框元素
            print("百度首页加载成功！")

            # 可选：自动在搜索框输入内容并搜索
            page.fill("#kw", "Playwright 自动化")  # 输入关键词
            page.click("#su")  # 点击搜索按钮

            # 等待搜索结果加载
            page.wait_for_selector(".result-op", timeout=8000)
            print("搜索完成！")

            # 保持浏览器打开 5 秒（让用户查看结果）
            time.sleep(5)

            # 关闭浏览器
            browser.close()

    except Exception as e:
        print(f"操作失败：{str(e)}")
        input("按回车键退出...")
        sys.exit(1)


if __name__ == "__main__":
    open_baidu_with_playwright()