import json
import numbers
import time
import traceback
import logging

from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
from django.views.decorators.csrf import csrf_exempt
import math

# Create your views here.
from tsetmc.models import Stock
from django.utils.timezone import now
from django.utils import timezone
import datetime

import pandas as pd
import finpy_tse as tse
from django.shortcuts import redirect
from urllib.parse import unquote

import requests
import urllib3

urllib3.disable_warnings()
from persiantools import characters





def convert_numb(text):
	import convert_numbers
	text = str(text)
	adad = -999999
	if text == "":
		adad = ""
		return adad
	elif text.find('(') != -1 and text.find('ریال') == -1 and text.find('=') == -1:
		adad = convert_numbers.persian_to_english(text)
		adad = int(adad) * -1
		return adad

	elif text.find('.') != -1:
		adad = text
		adad = adad[0:adad.find('.')]
		adad = text.replace(',', '')
		adad = int(float(adad))
		adad = convert_numbers.persian_to_english(adad)
		adad = int(adad)
		return adad
	elif text.find(',') != -1:
		adad = text.replace(',', '')
		adad = int(float(adad))
		adad = convert_numbers.persian_to_english(adad)
		adad = int(adad)
		return adad
	elif text.find('=') != -1:
		adad = text
		return adad
	elif text == "None":
		adad = ""
		return adad
	else:
		adad = convert_numbers.persian_to_english(text)
		adad = int(adad)
		return adad






@csrf_exempt
def api(request):
    # محاسبه نسبت

    import time
    import pandas as pd
    import finpy_tse as tse
    # import jdatetime
    # import openpyxl
    import string
    import os
    # import xlwt
    import shutil

    # def n2a(n, b=string.ascii_uppercase):
    #     d, m = divmod(n, len(b))
    #     return n2a(d - 1, b) + b[m] if d else b[m]

    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    # writepath = r'coef.xlsx'
    # if not os.path.exists(writepath):
    #     print(f'The file ({path_to_file}) does not exist')
    #     # original = r'C:/Users/mk/Desktop/ModaberAsia/back up 11/excel/Fund.xlsx'
    #     target2 = f'{target}coef.xlsx'
    #     shutil.copyfile(original, target2)
    #     print("file  created")

    # writepath = r'coef.xlsx'
    # if not os.path.exists(writepath):
    #     original = r'./template.xlsx'
    #     # target2 = f'{target}coef.xlsx'
    #     shutil.copyfile(original, writepath)
    #     print("file  created")

    def multple(ta):
        ta = int(ta)
        erorta = 0

        while True:
            try:
                logging.info(f'Get_MarketWatch')
                DF5 = tse.Get_MarketWatch(save_excel=False)
                logging.info(f'Get_MarketWatch done')

                break
            except Exception as e:
                erorta += 1
                print(
                    e, "\n", erorta, '**internet connection error , please check your internet or turn off your vpn**')
                logging.info(
                    f"{e} , {erorta} , **internet connection error , please check your internet or turn off your vpn**")
                time.sleep(10)

        li = pd.DataFrame(list(DF5)[0])
        li2 = pd.DataFrame(list(DF5)[1])

        namad = pd.DataFrame(pd.DataFrame(
            li2.index.tolist()).loc[:, 0]).drop_duplicates()
        namad = namad.reset_index().drop(columns=['index'])

        dict1 = {}

        while True:
            try:
                # listfilewb = "coef.xlsx"
                # wbkName = listfilewb
                # print("Excel location: ", wbkName)
                # wbk = openpyxl.load_workbook(wbkName)
                # wks = wbk['Sheet1']
                # wks["A" + str(1)].value = "نماد"
                # wks["B" + str(1)].value = "Buy/Sell"
                # wks["C" + str(1)].value = "R AND L"

                # wks[n2a(ta + 1) + str(1)].value = time.strftime("%H:%M:%S")
                for j in range(len(namad)):
                    try:

                        Buy_Price = li2.loc[namad.values[j]
                        [0]]['Buy-Price'].tolist()
                        Sell_Price = li2.loc[namad.values[j]
                        [0]]['Sell-Price'].tolist()

                        # if Buy_Price == li.loc[namad.values[j][0]].iloc[10]:
                        #     pass
                        Buy_Vol = li2.loc[namad.values[j][0]]['Buy-Vol'].tolist()
                        Sell_Vol = li2.loc[namad.values[j][0]]['Sell-Vol'].tolist()

                        high = li.loc[namad.values[j][0]].iloc[9]
                        low = li.loc[namad.values[j][0]].iloc[10]
                        Vol_Buy_I = li.loc[namad.values[j][0]].iloc[18]
                        Vol_Sell_I = li.loc[namad.values[j][0]].iloc[20]
                        Vol_Buy_R = li.loc[namad.values[j][0]].iloc[17]
                        Vol_Sell_R = li.loc[namad.values[j][0]].iloc[19]
                        No_Buy_R = li.loc[namad.values[j][0]].iloc[22]
                        No_Sell_R = li.loc[namad.values[j][0]].iloc[24]
                        Close = li.loc[namad.values[j][0]].iloc[5]
                        volume = li.loc[namad.values[j][0]].iloc[16]
                        popbuylist = []
                        popselllist = []

                        for xx, x in enumerate(Buy_Price):
                            if x > high and x != 0:
                                popbuylist.append(xx)
                                # print("Buy_Pricehigh", namad.values[j][0], xx, x)
                                # Buy_Price.pop(i)
                                # Buy_Vol.pop(i)
                            if x < low and x != 0:
                                # print("Buy_Pricelow", namad.values[j][0], xx, x)
                                popbuylist.append(xx)
                                # Buy_Price.pop(i)
                                # Buy_Vol.pop(i)

                        for yy, y in enumerate(Sell_Price):
                            if y > high and y != 0:
                                # print("Sell_Pricehigh", namad.values[j][0], yy, y)
                                popselllist.append(yy)
                                # Sell_Price.pop(u)
                                # Sell_Vol.pop(u)
                            if y < low and y != 0:
                                # print("Sell_Pricelow", namad.values[j][0], yy, y)
                                popselllist.append(yy)
                                # Sell_Price.pop(u)
                                # Sell_Vol.pop(u)

                        Buy_Price = [iii for jjj, iii in enumerate(Buy_Price) if jjj not in popbuylist]
                        Buy_Vol = [iii for jjj, iii in enumerate(Buy_Vol) if jjj not in popbuylist]

                        Sell_Price = [iii for jjj, iii in enumerate(Sell_Price) if jjj not in popselllist]
                        Sell_Vol = [iii for jjj, iii in enumerate(Sell_Vol) if jjj not in popselllist]

                        multiply_Buy = [Buy_Price[i] * Buy_Vol[i]
                                        for i in range(len(Buy_Price))]
                        multiply_Sel = [Sell_Price[i] * Sell_Vol[i]
                                        for i in range(len(Sell_Vol))]
                        Sum_Buy = sum(multiply_Buy)
                        Sum_Sel = sum(multiply_Sel)

                        power = (Vol_Sell_I - Vol_Buy_I) * Close
                        try:
                            powerreal = ((Vol_Buy_R / No_Buy_R) / (Vol_Sell_R / No_Sell_R))
                        except Exception as e:
                            powerreal = -1
                        if isfloat(str(power)):
                            power = float(str(power))
                        else:
                            power = 0

                        if math.isnan(power):
                            # print("power", power)
                            power = 0

                        if isfloat(str(powerreal)):
                            powerreal = float(str(powerreal))
                        else:
                            powerreal = 0

                        if math.isnan(powerreal):
                            # print("power", power)
                            powerreal = 0
                        if powerreal == math.inf:
                            powerreal = -1
                        # print(power)

                        try:
                            dict1[namad.values[j][0]] = {"id": j,
                                                         "name": namad.values[j][0],
                                                         "power": power,
                                                         "powerreal": powerreal,
                                                         "volume": volume,
                                                         "coef": int(Sum_Buy) / \
                                                                 int(Sum_Sel),
                                                         "time": time.strftime("%H:%M:%S"),
                                                         }

                        except ZeroDivisionError:
                            dict1[namad.values[j][0]] = {"id": j,
                                                         "name": namad.values[j][0],
                                                         "power": power,
                                                         "powerreal": powerreal,
                                                         "volume": volume,
                                                         "coef": -1,
                                                         "time": time.strftime("%H:%M:%S"),
                                                         }


                    except Exception as e:
                        print(namad.values[j][0])
                        logging.info(f"{namad.values[j][0]}")
                        print(traceback.format_exc())
                        logging.info(f" {traceback.format_exc()}")
                        # print(e)
                        # wks["A" + str(j + 2)].value = namad.values[j][0]
                        # wks[n2a(ta + 2) + str(j + 2)].value = -2

                # wbk.save(wbkName)
                print("Write Successfully")
                logging.info("Write Successfully")
                break
            except Exception as e:
                print(e)
                logging.info(f"{e}")
                # print(traceback.format_exc())
                print("\n--------------------------------")
                print(
                    "'fit.xlsx' is open OR excel file is crashed \nplease close 'fit.xlsx' to see update")
                print("--------------------------------\n")
                time.sleep(3)

        return dict1

    ta = 0
    # while True:
    ta += 1
    print("Time:" + str(time.strftime("%H:%M:%S")), "  Tedad:", ta)
    logging.info(f"Time:{time.strftime('%H:%M:%S')}  Tedad:{ta}")
    start = time.time()
    dict1 = multple(ta)
    end = time.time()
    # time.sleep(15)

    dictdata = Stock(data=dict1, name=get_client_ip(request))
    dictdata.save()
    print("Run Time1: ", end - start)
    logging.info(f"Run Time1: {end - start}")

    start = time.time()

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        print(len(data))
        logging.info(f"{len(data)}")

    coeflist = []
    powerlist = []
    vollist = []
    timelist = []
    dict2 = {}
    alldict = []

    # volco = Stock.objects.filter(name=get_client_ip(request),
    #                              created__gte=timezone.now() - timezone.timedelta(minutes=5))
    volco = Stock.objects.filter(
        created__gte=timezone.now() - timezone.timedelta(minutes=5))
    if volco.exists():
        try:
            print("volco", volco.count(), volco)
            logging.info(f"volco {volco.count()},,{volco}")
            volcolast = volco.last()
            volcofirst = volco.first()
            print("volcolast", volcolast, "volcofirst", volcofirst)
            logging.info(f"volcolast {volcolast},volcofirst,{volcofirst}")

            volcolast = volcolast.data
            volcolast = volcolast.replace("\'", "\"")
            volcolast = json.loads(volcolast)

            volcofirst = volcofirst.data
            volcofirst = volcofirst.replace("\'", "\"")
            volcofirst = json.loads(volcofirst)

            for ids, j in enumerate(volcolast.keys()):
                lastvm = volcolast[j]['volume']
                powerreal = volcolast[j]['powerreal']
                firstvm = volcofirst[j]['volume']
                try:
                    # print("lastvm", lastvm, "firstvm", firstvm, "nesbat", lastvm / firstvm)
                    pass
                except ZeroDivisionError:
                    # print("lastvm", lastvm, "firstvm", firstvm, "nesbat", 0)
                    pass


        except Exception as e:
            print(e)
            logging.info(f"{e}")

    data = Stock.objects.filter(
        created__gte=timezone.now() - timezone.timedelta(minutes=120))
    if data.exists():
        print("len(data)", len(data))
        logging.info(f"len(data){len(data)}")
        for i in data:
            dict1 = i.data
            dict1 = dict1.replace("\'", "\"")
            dict1 = json.loads(dict1)
            alldict.append(dict1)

        dict1 = alldict[0]
        for ids, j in enumerate(dict1.keys()):
            coeflist = []
            powerlist = []
            vollist = []
            timelist = []
            try:
                lastvm = volcolast[j]['volume']
                firstvm = volcofirst[j]['volume']
                powerreal = volcolast[j]['powerreal']

            except Exception as e:
                print(e)
                logging.info(f"{e}")
            try:
                # print("lastvm", lastvm, "firstvm", firstvm, "nesbat", lastvm / firstvm)
                nasbatvol = lastvm / firstvm
            except ZeroDivisionError:
                # print("lastvm", lastvm, "firstvm", firstvm, "nesbat", 0)
                nasbatvol = 0

            for idj, i in enumerate(alldict):
                # print("idj", idj, "ids", ids, "j", j, "i", i)
                try:
                    powerlist.append(alldict[idj][j]['power'])
                    vollist.append(alldict[idj][j]['volume'])
                    coeflist.append(alldict[idj][j]['coef'])
                    timelist.append(alldict[idj][j]['time'])

                    dict2[j] = {"id": ids,
                                "name": j,
                                "powerlast": powerlist[-1],
                                "powerreal": powerreal,
                                "volumelast": vollist[-1],
                                "coeflast": coeflist[-1],
                                "timelast": timelist[-1],
                                "power": powerlist,
                                "volume": vollist,
                                "nesbatvol": nasbatvol,
                                "coef": coeflist,
                                "time": timelist,
                                }
                except Exception as e:
                    # pass
                    print(e)
                    logging.info(f"{e}")
                    # print("idj", idj, "ids", ids, "j", j, "i", )

            # break

    # print(dict2)
    # print(powerlist)
    # print(vollist)

    end = time.time()
    print("Run Time2: ", end - start)
    logging.info(f"Run Time2: {end - start}")
    return JsonResponse(dict2, safe=False)


# @csrf_exempt
# def url(request, id):
#     print(type(id), id)
#     DF5 = tse.__Get_TSE_WebID__(str(id))
#     print(DF5, type(DF5))
#     ids = DF5.loc[:, 'WEB-ID'][0]
#     print(ids)
#     return redirect("http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=" + str(ids))


@csrf_exempt
def url(request, stock):
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}

    # search TSE function ------------------------------------------------------------------------------------------------------------
    def request(name):
        page = requests.get(f'http://www.tsetmc.com/tsev2/data/search.aspx?skey={name}', headers=headers)
        data = []
        for i in page.text.split(';'):
            try:
                i = i.split(',')
                data.append([i[0], i[1], i[2], i[7]])
            except:
                pass
        data = pd.DataFrame(data, columns=['Ticker', 'Name', 'WEB-ID', 'Active'])
        data['Name'] = data['Name'].apply(
            lambda x: characters.ar_to_fa(' '.join([i.strip() for i in x.split('\u200c')]).strip()))
        data['Ticker'] = data['Ticker'].apply(lambda x: characters.ar_to_fa(''.join(x.split('\u200c')).strip()))
        data['Name-Split'] = data['Name'].apply(lambda x: ''.join(x.split()).strip())
        data['Symbol-Split'] = data['Ticker'].apply(lambda x: ''.join(x.split()).strip())
        data['Active'] = pd.to_numeric(data['Active'])
        data = data.sort_values('Ticker')
        data = pd.DataFrame(data[['Name', 'WEB-ID', 'Name-Split', 'Symbol-Split']].values, columns=['Name', 'WEB-ID',
                                                                                                    'Name-Split',
                                                                                                    'Symbol-Split'],
                            index=pd.MultiIndex.from_frame(data[['Ticker', 'Active']]))
        return data

    # ---------------------------------------------------------------------------------------------------------------------------------
    if type(stock) != str:
        print('Please Enetr a Valid Ticker or Name1!')
        logging.info("Please Enetr a Valid Ticker or Name1!")

        return False
    # cleaning input search key
    stock = characters.ar_to_fa(''.join(stock.split('\u200c')).strip())
    first_name = stock.split()[0]
    stock = ''.join(stock.split())
    # search TSE and process:
    data = request(first_name)
    # logging.info(data)

    stock = unquote(stock)
    df_symbol = data[data['Symbol-Split'] == stock]
    df_name = data[data['Name-Split'] == stock]
    # logging.info(data['Symbol-Split'])
    # logging.info(data[data['Symbol-Split'] == "فارس"])
    # logging.info(data['Name-Split'])
    #
    # logging.info(df_symbol)
    # logging.debug(df_name)

    if len(df_symbol) > 0:
        print("omad inja 0")
        logging.info("omad inja 0")

        df_symbol = df_symbol.sort_index(level=1, ascending=False).drop(['Name-Split', 'Symbol-Split'], axis=1)
        # return df_symbol
        DF5 = df_symbol
        print(DF5, type(DF5))
        logging.info(DF5)

        ids = DF5.loc[:, 'WEB-ID'][0]
        print(ids)
        return redirect("http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=" + str(ids))
    elif len(df_name) > 0:
        print("omad inja 1")
        logging.info("omad inja 1")

        symbol = df_name.index[0][0]
        data = request(symbol)
        symbol = characters.ar_to_fa(''.join(symbol.split('\u200c')).strip())
        df_symbol = data[data.index.get_level_values('Ticker') == symbol]
        if len(df_symbol) > 0:
            print("omad inja 2")
            logging.info("omad inja 2")

            df_symbol = df_symbol.sort_index(level=1, ascending=False).drop(['Name-Split', 'Symbol-Split'], axis=1)
            # return df_symbol
            DF5 = df_symbol
            logging.info(DF5)
            print(DF5, type(DF5))
            ids = DF5.loc[:, 'WEB-ID'][0]
            print(ids)
            return redirect("http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=" + str(ids))
    print('Please Enetr a Valid Ticker or Name2!')
    logging.info("Please Enetr a Valid Ticker or Name2!")
    return False


@csrf_exempt
def api2(request):
    # api222222222222222222222222222222222222222222222
    start = time.time()

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        print(len(data))

    coeflist = []
    powerlist = []
    vollist = []
    timelist = []
    dict2 = {}
    alldict = []

    data = Stock.objects.filter(name=get_client_ip(request), created__gte=timezone.now() - timezone.timedelta(days=1))
    if data.exists():

        for i in data:
            dict1 = i.data
            dict1 = dict1.replace("\'", "\"")
            dict1 = json.loads(dict1)
            alldict.append(dict1)

        dict1 = alldict[0]
        for ids, j in enumerate(dict1.keys()):
            coeflist = []
            powerlist = []
            vollist = []
            timelist = []
            for idj, i in enumerate(alldict):
                powerlist.append(alldict[idj][j]['power'])
                vollist.append(alldict[idj][j]['volume'])
                coeflist.append(alldict[idj][j]['coef'])
                timelist.append(alldict[idj][j]['time'])

                dict2[j] = {"id": ids,
                            "name": j,
                            "powerlast": powerlist[-1],
                            "volumelast": vollist[-1],
                            "coeflast": coeflist[-1],
                            "timelast": timelist[-1],
                            "power": powerlist,
                            "volume": vollist,

                            "coef": coeflist,
                            "time": timelist,
                            }
            # break

    # print(dict2)
    # print(powerlist)
    # print(vollist)

    end = time.time()
    print("Run Time: ", end - start)
    return JsonResponse(dict2, safe=False)


def home1(request):
    # logging.error("home1 start")
    return render(request, 'home1.html')
    
    
    
    
    
    
def shome1(request):
    # logging.error("home1 start")
    return render(request, 'shome1.html')
    
    
    
    
    
@csrf_exempt
def surl(request, stock):
	print(stock)
	try:
		url="http://www.tsetmc.com/Loader.aspx?ParTree=151311&i="+stock
		return redirect(url)
	except Exception as e:
		return HttpResponse(e)


@csrf_exempt
def surl2(request, stock, is_saham):
	print(stock,is_saham)
	# read json from file if is not exist create it
	try:
		with open('saham.json', 'r') as f:
			data = json.load(f)
		# add new data to json
		data[stock] = is_saham
		# write json to file
		with open('saham.json', 'w') as f:
			json.dump(data, f)


	except:

		data = {}
		# add new data to json
		data[stock] = is_saham
		# write json to file
		with open('saham.json', 'w') as f:
			json.dump(data, f)



	return HttpResponse(stock+"-"+is_saham)


@csrf_exempt
def sapi(request):
	# محاسبه نسبت

	import time
	import pandas as pd
	import finpy_tse as tse
	# import jdatetime
	# import openpyxl
	import string
	import os
	# import xlwt
	import shutil

	# def n2a(n, b=string.ascii_uppercase):
	#     d, m = divmod(n, len(b))
	#     return n2a(d - 1, b) + b[m] if d else b[m]

	def isfloat(num):
		try:
			float(num)
			return True
		except ValueError:
			return False

	def get_client_ip(request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip

	# writepath = r'coef.xlsx'
	# if not os.path.exists(writepath):
	#     print(f'The file ({path_to_file}) does not exist')
	#     # original = r'C:/Users/mk/Desktop/ModaberAsia/back up 11/excel/Fund.xlsx'
	#     target2 = f'{target}coef.xlsx'
	#     shutil.copyfile(original, target2)
	#     print("file  created")

	# writepath = r'coef.xlsx'
	# if not os.path.exists(writepath):
	#     original = r'./template.xlsx'
	#     # target2 = f'{target}coef.xlsx'
	#     shutil.copyfile(original, writepath)
	#     print("file  created")

	import requests
	def Get_MarketWatch():
		import requests
		import pandas as pd

		# def Get_MarketWatch():
		# url = 'http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0'
		url = 'http://old.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0'

		r = requests.get(url)
		r.encoding = 'utf-8'
		data = r.text
		# print(data)
		data = data.replace('@', ';')
		data = data.split(';')
		data = [i.split(',') for i in data]
		data = pd.DataFrame(data)
		data = data.drop(data.index[0])
		data = data.dropna(axis=1, how='all')
		data = data.dropna(axis=0, how='all')
		data = data.dropna()
		try:
			data.columns = ["id", "id2", "نماد", "نام", "4", "اولین", "پایانی مقدار", "آخرین مقدار", "تعداد", "حجم",
							"ارزش",
							"کمترین", "بیشترین", "دیروز", "14", "حداقل قیمت مجاز", "16", "17", "18", "حداکثر قیمت مجاز",
							"حجم مبنا", "تعداد سهام", "دسته بندی", "0", "00"]
		except Exception as e:
			print(e)
			data.columns = ["id", "id2", "نماد", "نام", "4", "اولین", "پایانی مقدار", "آخرین مقدار", "تعداد", "حجم",
							"ارزش",
							"کمترین", "بیشترین", "دیروز", "14", "حداقل قیمت مجاز", "16", "17", "18", "حداکثر قیمت مجاز",
							"حجم مبنا", "تعداد سهام", "دسته بندی"]
			pass

		dfdf = data
		dfdf.to_excel("dfdf.xlsx")
		# display(dfdf)
		print(dfdf.shape)
		stockk = dfdf[dfdf["دسته بندی"] == "300"]
		# option = dfdf[dfdf["دسته بندی"] == "311" or dfdf["دسته بندی"] == "320"]
		option = dfdf[dfdf["دسته بندی"].isin(["311", "320", "312", "321", "0"])]
		print(option.shape)

		options = option[
			["id", "نماد", "نام", "پایانی مقدار", "آخرین مقدار", "تعداد", "حجم", "ارزش", "کمترین", "بیشترین", "دیروز",
			 "حداقل قیمت مجاز", "حداکثر قیمت مجاز"]]
		options.columns = ["id", "symbol", "name", "close_price", "last_price", "count", "volume", "value", "min_price",
						   "max_price", "yesterday", "min_price_allowed", "max_price_allowed"]

		options[["name1", "name2", "name3"]] = options["name"].str.split("-", expand=True)
		options["name1"] = options["name1"].str.replace("اختيارخ", "")
		options["name1"] = options["name1"].str.replace("ص آگاه", "اگاه")
		options["name1"] = options["name1"].str.replace("ص.دارا", "دارا")

		options["name1"] = options["name1"].str.strip()
		options["name2"] = options["name2"].str.strip()
		options["name3"] = options["name3"].str.strip()
		optionsdf = options.copy()
		options

		optionsNAMEs = options.name1.unique()
		optionsNAME = optionsNAMEs.tolist()
		optionsids = options.id.unique()
		optionsid = optionsids.tolist()

		# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

		from persiantools.jdatetime import JalaliDate
		from datetime import datetime

		def jal_to_jor(datesting):
			try:
				datesting = str(datesting)
				datesting = datesting.split("/")
				# print(datesting)
				rowyear = str(datesting[0])
				if len(str(rowyear)) > 3:
					rowyear = rowyear[-2:]
				# print(rowyear)
				if int(rowyear) > 50:
					year = int(f"13{rowyear}")
				else:
					year = int(f"14{rowyear}")
				# print(year)
				jordate = JalaliDate(year, int(datesting[1]), int(datesting[2])).to_gregorian()
				d0 = datetime.combine(jordate, datetime.min.time())
				delta = d0 - datetime.now()
				delta = delta.days
				return delta
			except Exception as e:
				# print(e)
				datesting = str(datesting)
				# extract betwin '
				datesting = datesting.split("'")[1]
				# split datesting 4 2 2 character
				datesting = [datesting[i:i + 2] for i in range(2, len(datesting), 2)]
				# print(datesting)
				rowyear = str(datesting[0])
				if len(str(rowyear)) > 3:
					rowyear = rowyear[-2:]
				# print(rowyear)
				if int(rowyear) > 50:
					year = int(f"13{rowyear}")
				else:
					year = int(f"14{rowyear}")
				# print(year)
				jordate = JalaliDate(year, int(datesting[1]), int(datesting[2])).to_gregorian()
				d0 = datetime.combine(jordate, datetime.min.time())
				delta = d0 - datetime.now()
				delta = delta.days
				return delta

		# jal_to_jor("1402/03/01")

		options["delta"] = options["name3"].apply(jal_to_jor)

		import requests
		import pandas as pd
		# url = 'http://www.tsetmc.com/tsev2/data/MarketWatchPlus.aspx?r=11833940375'
		url = 'http://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx?r=11833940375'

		r = requests.get(url)
		# r.encoding = 'utf-8'
		data = r.text
		# print(data)
		data = data.split('@', 1)[-1]
		data = data.replace('@', ';')
		data = data.split(';')
		data = [i.split(',') for i in data]
		data = pd.DataFrame(data)
		data = data.drop(data.index[0])
		data = data.dropna(axis=1, how='all')
		data = data.dropna(axis=0, how='all')
		data = data.sort_values(by=0)
		data.rename(columns={1: 'rowindex',
							 2: 'supnum',
							 3: 'demnum',
							 4: 'demprice',
							 5: 'supprice',
							 6: 'demvol',
							 7: 'supvol'
							 }, inplace=True)

		def id2price(id, index, verbose=False):

			spec = data[data[0] == f"{id}"]
			indexpanel = f"{index}"
			demprice = spec[spec["rowindex"] == indexpanel]["demprice"].values[0]
			supprice = spec[spec["rowindex"] == indexpanel]["supprice"].values[0]
			demvol = spec[spec["rowindex"] == indexpanel]["demvol"].values[0]
			supvol = spec[spec["rowindex"] == indexpanel]["supvol"].values[0]

			down = spec[spec[8].notnull()]
			fisrt = down["supnum"].values[0]
			close = down["supnum"].values[0]
			second = down["demprice"].values[0]
			totalnumber = down["supprice"].values[0]
			totalvolume = down["demvol"].values[0]
			totalvalue = down["supvol"].values[0]
			if verbose == True:
				print(demprice, supprice, demvol, supvol, fisrt, close, second, totalnumber, totalvolume, totalvalue)
			return demprice, supprice, demvol, supvol, fisrt, close, second, totalnumber, totalvolume, totalvalue

		for i in optionsNAME:
			try:
				id_namad = int(dfdf[dfdf["نماد"] == i]["id"].values[0])
				adj_close = int(dfdf[dfdf["نماد"] == i]["آخرین مقدار"].values[0])
				# print(i, id_namad)
				demprice, supprice, demvol, supvol, fisrt, close, second, totalnumber, totalvolume, totalvalue = id2price(
					id_namad, 1)
				options.loc[options['name1'] == i, 'orginal_close'] = adj_close
				options.loc[options['name1'] == i, 'panel_orginal_close'] = demprice
			except:
				adj_close = 0
				options.loc[options['name1'] == i, 'orginal_close'] = 0
				options.loc[options['name1'] == i, 'panel_orginal_close'] = 0

		for idd in optionsid:
			try:
				namad = dfdf[dfdf["id"] == idd]["نماد"].values[0]
				# print("ss", idd, namad)
				demprice, supprice, demvol, supvol, fisrt, close, second, totalnumber, totalvolume, totalvalue = id2price(
					idd, 1, verbose=True)
				options.loc[options['id'] == idd, 'panel_close'] = demprice
			except Exception as e:
				print(e)
				options.loc[options['id'] == idd, 'panel_close'] = 0

		# display(options)

		options["panel_close"] = options["panel_close"].apply(convert_numb)
		options["panel_orginal_close"] = options["panel_orginal_close"].apply(convert_numb)
		options["orginal_close"] = options["orginal_close"].apply(convert_numb)
		options["last_price"] = options["last_price"].apply(convert_numb)
		options["name2"] = options["name2"].apply(convert_numb)

		options["margin"] = options["panel_orginal_close"] - options["panel_close"]
		options["margin_percent"] = (options["name2"] - options["margin"]) / options["name2"] * 100
		options["margin_percent"] = options["margin_percent"].apply(lambda x: round(x, 2))
		options["margin_percent_monthly"] = (options["margin_percent"] / options["delta"]) * 30
		options["margin_percent_monthly"] = options["margin_percent_monthly"].apply(lambda x: round(x, 2))
		print(options["margin_percent_monthly"])
		# remove "" from margin_percent_monthly
		options["margin_percent_monthly"] = options["margin_percent_monthly"].apply(lambda x: str(x).replace("nan", ""))



		options["hedging"] = ((options["margin"] - options["name2"]) / options["name2"]) * 100
		options["hedging"] = options["hedging"].apply(lambda x: round(x, 2))
		def put_symbol(text):
			text = str(text)
			text = text.replace(text[0], "ط")
			return text

		options["put"] = options["symbol"].apply(put_symbol)

		# try:

		#     # options["put_price"] = options[options["symbol"] == options["put"]]["panel_close"]
		#     for i in options:
		#         print(i)
		#         if i["put"] in options["symbol"]:
		#             options["put_price"] = i["panel_close"]

		# except Exception as e:
		#     print(e)
		#     pass

		from persiantools import characters

		symblist = options["symbol"].to_list()
		symblist = list(map(characters.ar_to_fa, symblist))
		options["put_price"] = 0
		for i in range(len(options)):
			symb1 = characters.ar_to_fa(options["put"].iloc[i])
			if symb1 in symblist:
				options["put_price"].iloc[i] = options["panel_close"].iloc[i]
				# print(i)

		# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
		# options convert to dict
		options.reset_index(inplace=True, drop=True)
		options.reset_index(inplace=True)
		# options = options[
		# 	["index", "symbol", "name", "panel_close", "panel_orginal_close", "margin", "margin_percent", "delta",
		# 	 "margin_percent_monthly", "hedging", "put", "put_price"]]

		options = options[
			["id", "symbol", "name","panel_close", "panel_orginal_close", "margin", "margin_percent", "delta","margin_percent_monthly",
			  "hedging", "put", "put_price"]]
		# options["time"] = datetime.now().strftime("%H:%M:%S")
		options = options.sort_values(by="put_price", ascending=False)

		options["time"] = datetime.now().strftime("%H:%M:%S")
		options["check"] = False
		# read saham.json if id in key dict then put check in json
		with open('saham.json') as json_file:
			data = json.load(json_file)
			for i in data.keys():
				for j in options["id"]:
					if i == j:
						options.loc[options['id'] == j, 'check'] = data[i]

		options_dict = options.to_dict(orient='records')
		# return options_dict

		# options_dict
		# sort by delta
		# Get_MarketWatch()

		# options.head(50)
		# print(options)
		return options_dict

	datadict = Get_MarketWatch()

	return JsonResponse(datadict, safe=False)
