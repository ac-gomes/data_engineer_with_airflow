from services.get_data_api import GetAPIData

# from config.odds_api import config_test
# config_test()

recuperar_sportes = GetAPIData(request_type='sports')

data = recuperar_sportes.data_request()

print(data)
