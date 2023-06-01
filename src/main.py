from services.get_data_api import GetAPIData


recuperar_scores = GetAPIData('scores')

response = recuperar_scores.data_request()

print('\n', '------------------------------',
      response)


recuperar_sportes = GetAPIData('sports')

response = recuperar_sportes.data_request()

print('\n', '------------------------------',
      response)


# Response Headers
# x-requests-remaining   The number of requests remaining until the quota resets
# x-requests-used   The number of requests used since the last quota reset
