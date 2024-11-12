# -*- coding: utf-8 -*-

"""
fking pigai.org plus - using webdriver
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import configparser
import argparse

def driver_path(config: configparser.ConfigParser, driver: str,
                output_func=lambda x: print(x, end=''),
                reinstall: bool = False) -> (str, bool):
    if reinstall or not config.has_option(driver, 'path'):
        output_func('no available driver, downloading...')
        # download driver
        module = __import__(config.get(driver, 'package'),
                            fromlist=[config.get(driver, 'manager')])
        Manager = getattr(module, config.get(driver, 'manager'))
        config[driver]['path'] = Manager().install()
        output_func('Done.\n')
        reinstall = True
    return (config.get(driver, 'path'), reinstall)


def new_driver(config: configparser.ConfigParser, user_driver: str,
               output_func=lambda x: print(x, end=''),
               reinstall: bool = False) -> tuple:
    """新创建一个webdriver对象"""
    if user_driver == 'safari':
        # Safari不需要单独的驱动
        options = getattr(webdriver, user_driver).options.Options()
        options.add_experimental_option('detach', True)
        return (getattr(webdriver,
                        config.get(user_driver, 'driver'))(options=options),
                False)
    path, reinstall = driver_path(config, user_driver, output_func, reinstall)
    service = getattr(webdriver, user_driver).service.Service(path)
    options = getattr(webdriver, user_driver).options.Options()
    # 防止程序结束时浏览器关闭
    options.add_experimental_option('detach', True)
    return (getattr(webdriver,
                    config.get(user_driver, 'driver'))(service=service,
                                                       options=options),
            reinstall)


def login(config: configparser.ConfigParser, driver) -> bool:
    auto = True
    if config.has_option('user', 'username'):
        login_temp = driver.find_element(By.ID, 'username')
        config_user = config.get('user', 'username')
        login_temp.send_keys(config_user)
    else:
        auto = False
    if config.has_option('user', 'password'):
        login_temp = driver.find_element(By.ID, 'password')
        config_user = config.get('user', 'password')
        login_temp.send_keys(config_user)
    else:
        auto = False
    if auto:
        login_temp = driver.find_element(By.ID, 'ulogin')
        login_temp.click()
    return auto


def auto_login(driver, username, password) -> None:
    """通过提供参数自动登录"""
    login_temp = driver.find_element(By.ID, 'username')
    login_temp.send_keys(username)
    login_temp = driver.find_element(By.ID, 'password')
    login_temp.send_keys(password)
    login_temp = driver.find_element(By.ID, 'ulogin')
    login_temp.click()
    return

def get_homework(driver) -> list:
    """获取所有班级作文-名字获取失败了,只有id能用"""
    my_class = driver.find_element(By.ID, 'header_navi')
    my_class = my_class.find_element(By.LINK_TEXT, '班级')
    my_class.click()
    # fking pigai不好好写前端让我必须使用xpath定位
    elements = driver.find_elements(By.XPATH, '//*[@class="baseinfo flex"]')
    homework = []
    for element in elements:
        try:
            element = element.find_element(By.CLASS_NAME, 'flexbox')
            element = element.find_element(By.CLASS_NAME, 'flex')
            id_ = element.get_attribute('id')
            element = element.find_element(By.XPATH, '//*[@class="title ck"]')
            title = element.text
            homework.append((id_, title))
        except Exception:
            pass
    return homework


def homework_id(driver, id_: str) -> None:
    """通过作文号查询作文"""
    search = driver.find_element(By.NAME, 'rid')
    search.clear()
    search.click()
    search.send_keys(id_)
    button = driver.find_element(By.CLASS_NAME, 'sf_bt')
    button.click()
    return


def check_page(driver, id_: str = '', title: str = '') -> bool:
    """通过作文id或作文题目检查目标页面是否正确"""
    try:
        homework = driver.find_element(By.ID, 'timu')
    except Exception:
        return False
    homework = homework.text
    if id_:
        check = True if id_ in homework else False
    if title:
        check = True if title in homework else False
    return check


def get_request(driver) -> str:
    """获取作文要求"""
    request = driver.find_element(By.ID, 'request_y')
    return request.text


def auto_write(driver, title: str, contents: str) -> None:
    """写作文,必须保证页面是作文页面"""
    # title
    title_bar = driver.find_element(By.ID, 'title')
    title_bar.clear()
    title_bar.send_keys(title)
    # contents
    contents_bar = driver.find_element(By.ID, 'contents')
    contents_bar.click()
    contents_bar.send_keys(contents)
    return


def check_config(config: configparser.ConfigParser,
                 args: argparse.ArgumentParser().parse_args) -> tuple:
    """检查输入"""
    # driver
    if args.driver:
        driver = args.driver
    elif config.has_option('user', 'driver'):
        driver = config.get('user', 'driver')
    else:
        driver = ''
    if not driver in config.sections():
        print('Invalid driver. Choose one or renew config.')
        drivers = config.sections
        drivers.remove('user')
        driver = choose_driver(drivers)
    
    # login
    if args.username:
        username = args.username
    elif config.has_option('user', 'username'):
        username = config.get('user', 'username')
    else:
        username = input('Username: ')
        
    if args.password:
        password = args.password
    elif config.has_option('user', 'password'):
        password = config.get('user', 'password')
    else:
        password = input('Password: ')
    
    return (driver, username, password)


def choose_driver(drivers: list,
                  output_func=lambda x: print(x, end=''),
                  input_func=input) -> str:
    """由用户选择可用driver"""
    output_func('-'*20 + '\n\tAvailable Drivers:\n')
    for i in range(len(drivers)):
        output_func(f'  {i} > {drivers[i]}\n')
    input_ = input_func('Choose one(Default 0): ')
    return drivers[input_]


if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('id', type=str,
                        help='id of your homework on https://www.pigai.org')
    parser.add_argument('filename', type=str,
                        help='filename of your homework.')
    parser.add_argument('-t', '--title', type=str, default='',
                        help='title of your work. '
                        'Default: the same as name of your file')
    parser.add_argument('--username', type=str, default='',
                        help='login username. '
                        'Default: the same as username in config')
    parser.add_argument('--password', type=str, default='',
                        help='login password. '
                        'Default: the same as password in config')
    parser.add_argument('--config', type=str, default='./antiPIGAI_config.ini',
                        help='used config. Default: ./antiPIGAI_config.ini')
    parser.add_argument('--driver', type=str, default='',
                        help='used driver. '
                        'Default: the same as driver in config')
    parser.add_argument('--reinstall', action='store_true', default=False,
                        help='reinstall your web driver. Default: False')

    args = parser.parse_args()

    print('Using anti-pigai, reference and config template: '
          'https://github.com/sleepyHolo/antiPIGAI')
    config = configparser.ConfigParser()
    try:
        config.read(args.config)
    except Exception as e:
        print(e)
        exit()
    try:
        user_driver, username, password = check_config(config, args)
    
        driver, reinstall = new_driver(config, user_driver)
    
        driver.get('https://www.pigai.org')
    
        auto_login(driver, username, password)
        id_ = args.id
        homework_id(driver, id_)
        if check_page(driver, id_=id_):
            title = args.title if args.title else args.filename.split('.')[0]
            title = title.title()
            with open(args.filename, 'r') as file:
                text = file.read()
                auto_write(driver, title, text)
    
        if reinstall:
            # renew config
            with open(args.config, 'w') as configfile:
                config.write(configfile)
    except Exception as e:
        print(f'Error: {e}')
        print('Please check your input and config')
        print('You can also see https://github.com/sleepyHolo/antiPIGAI')
        exit()
