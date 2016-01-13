#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年1月12日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

Help:
'''
import conf
from model.goods import goods
from model.customer import customer





def alignment(str1, space, align = 'left', chars = None):
        if chars == None:
            chars = ' '
        length = len(str1.encode('gb2312'))
        space = space - length if space >=length else 0
        if align == 'left':
            str1 = str1 + chars * space
        elif align == 'right':
            str1 = chars* space +str1
        elif align == 'center':
            str1 = chars * (space //2) +str1 + chars* (space - space // 2)
        return str1




def print_main_menu():
    MAIN_MENU = ['血拼','查看购物车','退出']
    print('欢迎%s，您当前余额为%s。祝您购物愉快\n------------------------------------' %(current_user_info['username'], current_user_info['balance']))
    for i in range(len(MAIN_MENU)):
        print(" %s、%s " %(str(i+1).rjust(2), MAIN_MENU[i]))

def print_goods_list(goods_list, page = 1):
    list_index = []
    goods_list_page = goods_list[((page-1)*5):((page-1)*5+5)]
    print(' %s    %s%s    %s\n%s' %(alignment('商品编号',8), alignment('商品名称',50, ), alignment('价格',8, 'right'), '分类', ('-'*85)))
    for goods in goods_list_page:
        print(' %s    %s%s    %s' %(goods['id'].center(8), alignment(goods['name'],50), goods['price'].rjust(8), goods['class']))
        list_index.append(str(goods_list.index(goods)))
    print('-'*85)

    return list_index


def shopping():
    goods_list = goods.get_all_list()
    goods_count = len(goods_list)
    max_page = divmod(goods_count,5)[0] if divmod(goods_count,5)[1] == 0 else divmod(goods_count,5)[0]+1
    flag = True
    page = 1
    while flag:

        select_list = print_goods_list(goods_list, page)
        #print(select_list)
        print('当前是%s页/共%s页   %s' %(page, max_page, '退出血拼返回主菜单(r)  上一页(b)  下一页(n)'))
        chose = input('请输入商品编号加入购物车：')
        if chose in map(lambda x:str(int(x)+1),select_list):
            goods_name = goods_list[int(chose)-1]['name']
            goods_id = goods_list[int(chose)-1]['id']
            #print(goods_list[int(chose)-1])
            while True:

                confirm = input('您选择的是%s，\n请确认是否将其放入购物车(y/n)：' %goods_name)
                if confirm == 'y':
                    goods.add_to_shopping_cart(goods_id)
                    input('%s已放入购物车，\n按任意键继续购物' %goods_name)
                    break
                elif confirm == 'n':
                    input('%s已取消放入购物车，\n按任意键继续购物' %goods_name)
                    break
                else:
                    print('输入错误，请重新输入')
        elif chose == 'n':
            if page < max_page:
                page = page + 1
            else:
                input("已经是最后一页了，按任意键继续")
        elif chose == 'b':
            if page == 1:
                input("已经是第一页了，按任意键继续")
            else:
                page = page - 1
        elif chose == 'r':
            flag = False
        else:
            input("输入错误，按任意键继续")





def show_shopping_cart():
    total = 0
    #print(goods.get_shopping_cart())
    print(' %s    %s%s    %s%s\n%s' %(alignment('商品编号',8), alignment('商品名称',50), alignment('单价',8, 'right'), alignment('个数',8, 'right'), alignment('小计',8, 'right'), '-'*95))
    res = goods.get_shopping_cart()
    if len(res) != 0:
        for cart_list in res:
            total = total + cart_list['subtotal']
            print(' %s    %s%s    %s%s' %(cart_list['id'].center(8), alignment(cart_list['name'],50), str(cart_list['price']).rjust(8), str(cart_list['num']).rjust(8), str(cart_list['subtotal']).rjust(9)))
    else:
        print('您的购物车空空如也，快去血拼吧')
    print('-'*95)
    print('总计：%s'.rjust(95-len(str(total))) % total)
    print('操作： 结账(p)    返回上级菜单(r)    清空购物车(e)    删除商品(d)')
    return total


def shoppin_cart():
    while True:
        total = show_shopping_cart()
        #print(total)
        chose = input("请选择您的操作：").strip()
        if chose == 'e':
            if total != 0:
                confirm = input('请确认是否确认确认是否清空购物车（y）：').strip()
                if confirm == 'y':
                    goods.del_all_cart()
                    input('购物车已经清空，按任意键继续')
                else:
                    input('清空购物车已经取消，按任意键继续')
            else:
                input('购物车是空的，快去血拼吧，按任意键继续')

        elif chose == 'p':
            if total != 0:
                if total <= int(current_user_info['balance']):
                    customer.pay(total)
                    goods.del_all_cart()
                    input('完成支付，谢谢。按任意键返回主菜单')
                    break
                else:
                    input('您当前余额不足无法支付，请删除部分商品，按任意键继续')
            else:
                input('购物车是空的，快去血拼吧，按任意键继续')
        elif chose == 'r':
            break
        elif chose == 'd':
            pass


if __name__ == '__main__':
    goods = goods(conf.goods_file)
    #print(goods.get_list())
    customer = customer(conf.customer_file)
    print(conf.app_info)
    print('请先登录：')
    if customer.authenticate():
    #if True:
        current_user_info = customer.get_current_customer_info()
        flag = True
        while flag:
            print_main_menu()
            chose = input("请输入菜单编号：").strip()
            if chose == '1':
                shopping()
            elif chose == '2':
                shoppin_cart()
            elif chose == '3':
                flag = False
                print('欢迎您下次再来，再见！')
            else:
                input('输入错误，请重新输入，按任意键继续')