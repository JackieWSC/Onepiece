import pandas as pd

def dump_sumary(ad_report, ad_rule, result):
    print("ad_report dimensions: {}".format(ad_report.shape))
    print("ad_rule dimensions: {}".format(ad_rule.shape))
    print("result dimensions: {}".format(result.shape))
    print(result.head(10))


def exe_ad_rule_1(ad_report, ad_rule):
    result = pd.merge(ad_report,
                      ad_rule,
                      on=['LineItemType', 'CreativeSize']).drop('Description', axis=1)

    dump_sumary(ad_report, ad_rule, result)

    return result


def exe_ad_rule_2(ad_report, ad_rule):
    result = pd.merge(ad_report,
                      ad_rule,
                      on=['LineItemType', 'InventoryTypes', 'CreativeSize']).drop('Description', axis=1)

    dump_sumary(ad_report, ad_rule, result)

    return result


def exe_ad_rule_3(ad_report, ad_rule):
    temp = set()
    for x in ad_rule.AdUnit:
        temp.add(x)

    pat = '|'.join(r"{}".format(x) for x in temp)
    print('pat:{}'.format(pat))
    ad_report['AdUnit_contains'] = ad_report.AdUnit.str.extract('(' + pat + ')', expand=False)
    # print(ad_report.head())

    result = pd.merge(ad_report,
                      ad_rule,
                      left_on=['LineItemType', 'InventoryTypes', 'CreativeSize', 'AdUnit_contains'],
                      right_on=['LineItemType', 'InventoryTypes', 'CreativeSize', 'AdUnit'],
                      suffixes=('', '_y')).drop(['AdUnit_contains', 'AdUnit_y', 'Description'], axis=1)

    dump_sumary(ad_report, ad_rule, result)

    return result


def exe_ad_rule_4(ad_report_temp, ad_rule):
    temp = set()
    for x in ad_rule.Creative_Size_Delivered:
        temp.add(x)

    pat = '|'.join(r"{}".format(x) for x in temp)
    print('pat:{}'.format(pat))
    ad_report_temp['Creative_Size_Delivered_contains'] = \
        ad_report_temp.Creative_Size_Delivered.str.extract('(' + pat + ')', expand=False)
    # print(ad_report.head())

    result = pd.merge(ad_report_temp,
                      ad_rule,
                      left_on =['LineItemType', 'Creative_Size_Delivered_contains'],
                      right_on=['LineItemType', 'Creative_Size_Delivered'],
                      suffixes=('', '_y')).drop(['Creative_Size_Delivered_contains', 'Creative_Size_Delivered_y', 'Description'], axis=1)

    dump_sumary(ad_report_temp, ad_rule, result)

    return result

# main

# pandas setting
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# load csv
ad_report = pd.read_csv("report.csv")
ad_rule_1 = pd.read_csv("ad_rule_1.csv")
ad_rule_2 = pd.read_csv("ad_rule_2.csv")
ad_rule_3 = pd.read_csv("ad_rule_3.csv")

# apply the rule
ad_rule_1_result = exe_ad_rule_1(ad_report.copy(), ad_rule_1)
ad_rule_2_result = exe_ad_rule_2(ad_report.copy(), ad_rule_2)
ad_rule_3_result = exe_ad_rule_3(ad_report.copy(), ad_rule_3)


# concat result
result = pd.concat([ad_rule_1_result,
                    ad_rule_2_result,
                    ad_rule_3_result])
print("result dimensions: {}".format(result.shape))
result.to_csv('ad_result.csv')
