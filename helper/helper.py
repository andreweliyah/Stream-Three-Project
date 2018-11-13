def check(request):
  import requests
  payload = {'token': request.COOKIES.get('jwtoken')}
  r = requests.post(request.scheme + '://' + request.get_host() + '/api-token-verify/', data=payload)
  if r.status_code != 200 :
    return False
  return True