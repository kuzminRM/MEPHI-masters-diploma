import requests

r_filter_25kg = requests.get(
    'https://api-ecomm.sdvor.com/occ/v2/sd/products/search?'
    'fields=algorithmsForAddingRelatedProducts%2CcategoryCode%2Cproducts(code%2Cslug%2CdealType%2Cname%2Cunit%2Cunits(FULL)%2CunitPrices(FULL)%2CavailableInStores(FULL)%2Cbadges(DEFAULT)%2Cmultiunit%2Cprice(FULL)%2CcrossedPrice(FULL)%2CtransitPrice(FULL)%2CpersonalPrice(FULL)%2Cimages(DEFAULT)%2Cstock(FULL)%2CmarketingAttributes%2CisArchive%2Ccategories(FULL)%2CcategoryNamesForAnalytics)%2Cfacets%2Cbreadcrumbs%2Cpagination(DEFAULT)%2Csorts(DEFAULT)%2Cbanners(FULL)%2CfreeTextSearch%2CcurrentQuery%2CkeywordRedirectUrl&'
    'currentPage=0&'
    'pageSize=18&'
    'facets=allCategories%3Ashtukaturki-5584%2Cfacet_attr-ves_cl-l3-shtukaturki%3A25.0&'
    'lang=ru&'
    'curr=RUB&'
    'deviceType=tablet&'
    'baseStore=moscow'
)
r = requests.get(
    'https://api-ecomm.sdvor.com/occ/v2/sd/products/search?'
    'fields=algorithmsForAddingRelatedProducts%2CcategoryCode%2Cproducts(code%2Cslug%2CdealType%2Cname%2Cunit%2Cunits(FULL)%2CunitPrices(FULL)%2CavailableInStores(FULL)%2Cbadges(DEFAULT)%2Cmultiunit%2Cprice(FULL)%2CcrossedPrice(FULL)%2CtransitPrice(FULL)%2CpersonalPrice(FULL)%2Cimages(DEFAULT)%2Cstock(FULL)%2CmarketingAttributes%2CisArchive%2Ccategories(FULL)%2CcategoryNamesForAnalytics)%2Cfacets%2Cbreadcrumbs%2Cpagination(DEFAULT)%2Csorts(DEFAULT)%2Cbanners(FULL)%2CfreeTextSearch%2CcurrentQuery%2CkeywordRedirectUrl&'
    'currentPage=0&'
    'pageSize=18&'
    'facets=allCategories%3Ashtukaturki-5584&'
    'lang=ru&'
    'curr=RUB&'
    'deviceType=tablet&'
    'baseStore=moscow'
)
j = r.json()

menu = 'https://api-ecomm.sdvor.com/occ/v2/sd/cms/menu?fields=DEFAULT&nodeId=SdCategoryNavNode&level=1&lang=ru&curr=RUB&deviceType=tablet&baseStore=moscow'
menu2 = 'https://api-ecomm.sdvor.com/occ/v2/sd/cms/menu?fields=DEFAULT&nodeId=stroitelnye-materialy-5521NavNode&level=1&lang=ru&curr=RUB&deviceType=tablet&baseStore=moscow'
menu3 = 'https://api-ecomm.sdvor.com/occ/v2/sd/cms/menu?fields=DEFAULT&nodeId=stroitelnye-smesi-gruntovki-10991NavNode&level=1&lang=ru&curr=RUB&deviceType=tablet&baseStore=moscow'
