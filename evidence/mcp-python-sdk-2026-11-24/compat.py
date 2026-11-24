import asyncio,json,importlib.metadata,datetime,base64
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
URL='https://acq.damri.org/mcp'
def log(stage,value):
 print(json.dumps({'stage':stage,'value':value},default=str),flush=True)
async def main():
 log('environment',{'sdk':'mcp','version':importlib.metadata.version('mcp'),'endpoint':URL,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'official SDK client compatibility, no model agents'})
 async with AsyncExitStack() as stack:
  sessions=[]
  for seat in ['A','B']:
   streams=await stack.enter_async_context(streamable_http_client(URL))
   s=await stack.enter_async_context(ClientSession(streams[0],streams[1],read_timeout_seconds=30))
   init=await s.initialize(); log('initialize_'+seat,init.model_dump(mode='json'));sessions.append(s)
  a,b=sessions
  tools=await a.list_tools();log('tools',[{'name':x.name,'inputSchema':x.input_schema} for x in tools.tools])
  async def call(s,name,args):
   r=await s.call_tool(name,args)
   assert not r.is_error,(name,r)
   texts=[x.text for x in r.content if x.type=='text']
   data=json.loads(texts[0]);return data
  created=await call(a,'acq_create_room',{'topic':'Fictional SDK compatibility test, no model agents','join_window_hours':0.1})
  # Do not persist invitation/seat/recovery credentials in shareable evidence.
  log('create_A',{k:v for k,v in created.items() if k in ['roomId','expiresAt','joinBy','topic']})
  uin=created['roomId'];ta=created.get('token') or json.loads(base64.urlsafe_b64decode(created['credential'][5:]+'==='))['token']
  joined=await call(b,'acq_join_room',{'uin':uin});tb=joined['token']
  log('join_B',{'joined':True,'seat':joined.get('seat')})
  msg='Fictional compatibility check: blue kite is ready.'
  sent=await call(a,'acq_send',{'uin':uin,'token':ta,'text':msg,'cid':'sdk-compat-A1'});log('send_A',sent)
  got=await call(b,'acq_recv',{'uin':uin,'token':tb,'since':0,'peek':True});log('recv_B',got)
  assert msg in json.dumps(got)
  reply='Fictional compatibility reply: blue kite received.'
  log('send_B',await call(b,'acq_send',{'uin':uin,'token':tb,'text':reply,'cid':'sdk-compat-B1'}))
  gota=await call(a,'acq_recv',{'uin':uin,'token':ta,'since':0,'peek':True});log('recv_A',gota)
  assert reply in json.dumps(gota)
  log('end_room',await call(a,'acq_send',{'uin':uin,'token':ta,'text':'Fictional SDK compatibility test complete.','end':True,'cid':'sdk-compat-end'}))
  log('PASS',{'sessions':2,'model_agents':0,'bidirectional':True})
asyncio.run(main())
