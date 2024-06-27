import openai

# Modify OpenAI's API key and API base to use vLLM's API server.
openai.api_key = "EMPTY"
openai.api_base = "http://222.128.48.7:18000/v1"

# List models API
models = openai.Model.list()
print("Models:", models)

model = models["data"][0]["id"]
detail = '''Issuance
EUR/GBP Issuance 
In our 2019 outlook piece (here), we highlighted our expectations for at least €45bn 
of combined TMT issuance led by €30bn+ in the TelCo space. While our TelCo 
expectations have paced as expected, pending M&A could skew that decently higher
(TMUS in December said it could issue ~$19bn of new secured IG notes across USD 
and EUR markets when “we have surety from a regulatory standpoint that we can 
proceed with this merger”). Our prior Technology estimate (€10bn) has already been 
surpassed with IBM (€5bn in regular-way issuance), Fidelity National (€5bn and 
£1.25bn for M&A), and Fiserv (€1.5bn and £1.05bn for M&A) all bringing sizable 
Reverse Yankee deals which we had not factored into our estimates. Media has
finally picked up after recent issuance from Publicis, Vivendi, and Eutelsat for M&A 
and refi purposes. We see favorable cross-currency dynamics in Europe (for issuers)
continuing to support Reverse Yankee supply, highlighting a recently announced 
inaugural Omnicom (OMC) mandate. As such, we now target an aggregate ~€65bn in 
TMT issuance. This is led by TelCos (€35bn), with €10bn expected from Media and 
€20bn from Technology (though that total could easily skew towards €70bn+ if some 
pending M&A deals are approved). We specifically highlight increased funding 
needs for issuers involved in the German spectrum auction, refinancing for America 
Movil and Bouygues, and advantageous issuance from our largest Telecoms 
(particularly BT Group). In Media and Technology, we believe Infineon, Wolters 
Kluwer, and JCDecaux may aim to fund M&A later this year, and expect SES to tap 
the markets for refinancing needs. 
USD Issuance
Technology issuance YTD in 2019 has tracked ahead of our expectations largely 
driven by the increased pace of consolidation in the payments sub-sector and 
increased supply in the semiconductor space. We are thus revising our target for 
2019 Technology issuance to $83bn from $73bn previously as we anticipate M&A 
activity to continue, although at a more moderate pace, and assume that our cash-rich 
issuers will pay down 2019 maturities and fund buybacks with cash on hand. In the 
Media & Entertainment sector, we continue to expect 2019 new supply of ~$25bn
(currently $11.75bn YTD). We expect very limited new cable supply (~$4bn-5bn) 
for the rest of 2019 largely driven by potential refinancing of Comcast maturities and 
issuance for share repurchases at Charter. We expect new Media supply of ~$10bn 
for the second half of 2019. A large portion of our estimate derives from Disney
terming out bridge financing from the 21st Century Fox transaction, net of the RSN 
proceeds. While M&A activity will likely continue in the Media sector, we don’t see 
any material trades funded in the debt market during the second half of the year. In 
the Telecom space, domestic issuance of $12.9bn has been light YTD, which is in
line with our low expectations for new issuance due to a relative lack of supply from 
AT&T and Verizon. Yankee Telecom issuance of ~$5.5bn is more in line with 
historical levels following an abnormally high issuance year in 2018 driven by 
Vodafone’s funding for the purchase of Liberty Global’s continental European assets.
'''
print(len(detail))
prompt = '''
USER:你是一位专业投资人，擅长采取自问自答的形式从研报中找到行业内部逻辑，你回答用户的问题详细而又细心。
'''+detail+'''
这是一份研究报告，请根据该研报创建json格式的多个问答对。其中，问题部分需要包含背景，将代词替换为实体，使得看到你问答对的人可以不用看报告就可以理解。格式如下：
[{'Question':'', 
'Answer':''},……]

ASSISTANT::
'''
# Completion API
stream = False
completion = openai.Completion.create(
    model=model,
    prompt=prompt,
    echo=False,
    n=2,
    # ignore_eos=False,
    max_tokens = 1024,
    stream=stream,
    logprobs=3)

print("Completion results:")
if stream:
    for c in completion:
        print(c)
else:
    print(completion)
    print(completion.get('choices')[0].get('text').encode('utf-8').decode('utf-8').split('</s>')[0])