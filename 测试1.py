import pyautogui
import time
import cv2
import numpy as np
from datetime import datetime, timedelta
import keyboard
import traceback
import os
import threading
import sys

# 设置失败安全，将鼠标移到屏幕左上角将中断程序
pyautogui.FAILSAFE = True

# 添加退出标志
exit_program = False

# 监听ESC键的函数
def check_for_exit():
    global exit_program
    print("开始监听ESC键，按ESC可随时退出程序...")
    while True:
        if keyboard.is_pressed('esc'):
            print("检测到ESC键，程序即将退出...")
            exit_program = True
            break
        time.sleep(0.1)  # 降低CPU使用率

def find_image_on_screen(template_path, screenshot=None, confidence=0.8):
    """
    在屏幕上查找模板图像的位置，并在找到时绘制矩形框
    
    Args:
        template_path: 模板图像的路径
        screenshot: 可选的屏幕截图，如果为None则自动截取
        confidence: 匹配置信度
        
    Returns:
        如果找到图像，返回(x, y, w, h)，否则返回None
        同时返回处理后的截图
    """
    try:
        # 截取全屏
        screenshot = pyautogui.screenshot()
        #保存截图
        screenshot.save('screenshot1.png')
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        
        # 读取模板图像
        template = cv2.imread(template_path)
        if template is None:
            print(f"无法读取模板图像: {template_path}")
            return None, screenshot
        
        # 获取模板图像的宽度和高度
        h, w = template.shape[:2]
        
        # 模板匹配
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
          
        
        # 查找匹配超过阈值的位置
        loc = np.where(result >= confidence)
        
        # 如果找到匹配
        if len(loc[0]) > 0:
            # 获取最佳匹配点
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            
            # 在截图上绘制矩形框
            img_with_rect = screenshot.copy()
            cv2.rectangle(img_with_rect, top_left, bottom_right, (0, 0, 255), 2)  # 红色矩形，线宽为2
            
            
            # 保存带有矩形框的截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"matched.png"
            cv2.imwrite(save_path, img_with_rect)
            print(f"带有匹配区域标记的截图已保存为 '{save_path}'")
            
            return (top_left[0], top_left[1], w, h), img_with_rect
        
        return None, screenshot
    except Exception as e:
        print(f"查找图像时出错: {e}")
        return None, screenshot

def handle_practice_window(screenshot):
    """处理练习弹窗"""
    print("检测到练习弹窗，开始点击选项...")
    
    # 依次点击选项和关闭按钮
    points = [(712, 562), (711, 627), (710, 687), (707, 751), (964, 843)]
    for point in points:
        pyautogui.click(point[0], point[1])
        time.sleep(0.5)
    
    # 等待3秒后再次点击关闭按钮
    time.sleep(3)
    pyautogui.click(964, 843)
    print("练习弹窗处理完成")
    return True  # 返回True表示已处理事件

def move_to_next_video(screenshot):
    """移动到下一个视频"""
    print("切换到下一个视频...")
    
    # 寻找当前视频播放按钮
    current_button, marked_screenshot = find_image_on_screen("current-pbt.png", screenshot)
    if current_button:
        # 计算中心坐标
        center_x = current_button[0] + current_button[2] // 2
        center_y = current_button[1] + current_button[3] // 2
        
        # 移动到按钮中心
        pyautogui.moveTo(center_x, center_y)
        
        # 向下滚动60
        pyautogui.scroll(-60)  # 负值表示向下滚动
        time.sleep(1)  # 等待滚动完成
        
        # 点击当前位置 (下一个视频)
        pyautogui.click()
        time.sleep(2)
        if find_image_on_screen("end-play.png", screenshot)[0]:
                
                # 向下滚动60
                pyautogui.scroll(-60)  # 负值表示向下滚动
                time.sleep(1)  # 等待滚动完成
                
                # 点击当前位置 (下一个视频)
                pyautogui.click() 
                time.sleep(2)
                # pyautogui.click(964, 843)
                # quiken()
        pyautogui.click(964, 843)
        quiken()


        print("已切换到下一个视频")
    else:
        print("未找到当前视频播放按钮")
        return False  # 返回False表示未能切换到新视频

def handle_unit_test(screenshot):
        """处理单元测试"""
        print("检测到单元测试...")
        
        # 移动到中心
        pyautogui.moveTo(82, 16)
        pyautogui.click()
        time.sleep(0.5)
        
        # 寻找当前视频播放按钮
        current_button, marked_screenshot = find_image_on_screen("current-pbt.png", screenshot)
        if current_button:
            # 计算中心坐标
            center_x = current_button[0] + current_button[2] // 2
            center_y = current_button[1] + current_button[3] // 2
            
            # 移动到按钮中心
            pyautogui.moveTo(center_x, center_y)
            
            # 向下滚动210
            pyautogui.scroll(-210)  # 负值表示向下滚动
            time.sleep(1)  # 等待滚动完成
            
            # 点击当前位置 (下一个视频)
            pyautogui.click()
            time.sleep(2)
            pyautogui.click(964, 843)
            time.sleep(2)
            quiken()
            print("已切换到下一个视频")
            print("单元测试处理完成")
            return True  # 返回True表示已处理事件
def judge_cuorse_warning(screenshot):   
    """判断是否出现课程提醒"""
    course_warning, marked_screenshot = find_image_on_screen("course-warning.png", screenshot)
    if course_warning:
            time.sleep(1)
            pyautogui.click(1174, 764)
            pyautogui.moveTo(1703, 829) #移动一下鼠标
            time.sleep(0.5)
            pyautogui.scroll(100)

        
def quiken():
     pyautogui.moveTo(1000, 843) #移动一下鼠标
     time.sleep(0.5)
     pyautogui.moveTo(1234, 962)
     time.sleep(0.5)
     pyautogui.moveTo(1234, 799)
     pyautogui.click()
     time.sleep(0.5)

def main():
    """主函数"""
    global exit_program
    
    # 启动ESC键监听线程
    exit_thread = threading.Thread(target=check_for_exit)
    exit_thread.daemon = True  # 设置为守护线程，主线程结束时会自动终止
    exit_thread.start()
    
    print("程序启动，等待20秒后开始...")
    time.sleep(20)  # 初始等待20秒
    pyautogui.click(964, 843)
    time.sleep(1.5)
    quiken()
    
    print("开始监控...")
    restart_timer = True
    
    while not exit_program:  # 循环条件改为检查退出标志
        try:
            screenshot = np.array(pyautogui.screenshot())
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            
            # 情况1: 检查是否有练习弹窗
            practice_window, marked_screenshot = find_image_on_screen("practice-window.png", screenshot)
            if practice_window:
                print("1111")
                handle_practice_window(marked_screenshot)
                # 处理完弹窗后继续当前视频，不重置计时器
            
            # 情况2: 检查是否到达视频结束
            elif find_image_on_screen("end-play.png", screenshot)[0]:
                print("2222")
                print("检测到视频结束")
                if move_to_next_video(screenshot):
                    restart_timer = True  # 重置计时器标志
                
            # 情况3: 检查是否有单元测试
            elif find_image_on_screen("unit-test.png", screenshot)[0]:
                print("3333")
                if handle_unit_test(screenshot):
                    restart_timer = True
            elif find_image_on_screen("course-warning.png", screenshot)[0]:
                print("4444")
                judge_cuorse_warning(screenshot)      
            
            # 检查是否应该退出
            if exit_program:
                break
                
            # 等待10秒后再次检查
            time.sleep(10)
            
        except Exception as e:
            print(f"循环中出错: {e}")
            traceback.print_exc()
            # 如果发生错误但未设置退出标志，继续运行
            if not exit_program:
                time.sleep(5)
                continue
            else:
                break

    print("程序正常退出")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("程序被用户中断")
    except Exception as e:
        print(f"程序出错: {e}")
        traceback.print_exc()
    finally:
        print("程序已终止")
