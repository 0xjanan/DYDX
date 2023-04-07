import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests as r
from datetime import datetime
import time

st.set_page_config(page_title='dYdX token activity',layout='wide',page_icon="chart_with_upwards_trend")

# Data Sources
@st.cache(ttl=86400, allow_output_mutation=True)
def get_data(query):
    if query == 'dydx price':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/ecca7d16-3ed5-4870-8229-6fe44350ece5/data/latest')
    elif query == 'Holders':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/de06666e-ca1a-4939-a3d7-38acd0462f26/data/latest')
    elif query == 'dist':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/c9eec574-ed11-41a0-8187-47225293cf8c/data/latest')
    elif query == 'dist overtime':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/6e18b3e0-3128-4c9f-88e5-86e3250651a2/data/latest')
    elif query == 'holdc':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/6b34034b-752b-4414-baec-1f89320290e9/data/latest')
    elif query == 'stak':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/a845a423-9049-4251-ab47-f83b0abe6fe4/data/latest')
    elif query == 'cex':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/1d54d4a6-9aac-4de6-9871-aecb4c469ac2/data/latest')
    elif query == 'swaps':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/c221f673-4f2a-4cd9-b58a-0e64e51a2c14/data/latest')
    elif query == 'dydx info':
        return r.get("https://api.coingecko.com/api/v3/coins/dydx").json()
    
    return None

dydx_p = get_data('dydx price')
dydx_p2 = get_data('dydx info')
holders = get_data('Holders')
dist = get_data('dist')
dist_overtime = get_data('dist overtime')
current_hold = get_data('holdc')
stak = get_data('stak')
cex = get_data('cex')
swaps = get_data('swaps')

dydx_price = dydx_p2['market_data']['current_price']['usd']
dydx_cirs = round(dydx_p2['market_data']['circulating_supply'],2)
dydx_mrkcp = dydx_p2['market_data']['market_cap']['usd']
dydx_fdv = dydx_p2['market_data']['fully_diluted_valuation']['usd']
p_ch = round(dydx_p2['market_data']['price_change_24h'],2)
m_ch = round(dydx_p2['market_data']['market_cap_change_24h'],2) 
ttl_supply = 1000000000
updt = dydx_p2['market_data']['last_updated']
ath = dydx_p2['market_data']['ath']['usd']
atl = dydx_p2['market_data']['atl']['usd']

date_object = datetime.strptime(updt, "%Y-%m-%dT%H:%M:%S.%fZ")
date_ = date_object.strftime("%Y-%m-%d")
tvl = dydx_p2['market_data']['total_value_locked']['usd']

st.title('dYdX token activity')
st.markdown('''
### Introduction
---

DYDX is a decentralized exchange (DEX) for trading and lending digital assets built on the Ethereum blockchain. It utilizes smart contracts to allow users to trade and borrow assets in a trustless and decentralized way. The platform enables trading of various ERC-20 tokens, and it also offers margin trading and lending services with the use of their native DYDX token. DYDX token holders can also participate in governance of the protocol.


---
### Methodology
dYdX's token contract address is `0x92d6c1e31e14520e676a687f0a93788b716beff5` and with the help of Flipside Crypto, we use the 'ethereum.core' table to find out the price of this token, holders, staking actions, swapping volume, and finally transfers. Which is calculated and visualized as below to find out the impact of major DYDX token release on the market. As we could find the previous on chain data of users behavior.
Besides of those on-chain data, I gathered some data from Coingecko api to help us get overall idea of the token.
''')

st.markdown('''
---
## General 
''')

u1, u2, u3 = st.columns(3)
with u1:
    u1.metric("DYDX Price (USD)",dydx_price, delta=f'{p_ch:,}',help='last 24 hours')
    u1.metric("Last updated", date_)
    u1.metric("All Time High",ath,help='USD')
with u2:
    u2.metric("DYDX Marketcap (USD)",f'{dydx_mrkcp:,}',delta=f'{m_ch:,}',help='last 24 hours')
    u2.metric("DYDX FDV (USD)", f'{dydx_fdv:,}',help='Fully Diluted Valuation')
    u2.metric("All Time Low",atl,help='USD')
with u3:
    u3.metric("DYDX Circulation",f'{dydx_cirs:,}',help='last 24 hours')
    u3.metric("Total Supply",f'{ttl_supply:,}')
    u3.metric("Total Value Locked",f'{tvl:,}',help='USD')

st.markdown('''
''')
  


fig = px.line(
    dydx_p,
    x='DAYS',
    y='PRICE',
    title='DYDX Daily Price',
    color=px.Constant("DYDX Price"),
    labels=dict(color="Price")
    
    )
fig.update_layout( hovermode='x unified')
st.plotly_chart(
    fig,
    use_container_width=True)

c1,c2 = st.columns(2)
with c1:
    figj = px.bar(
        holders,
        x='DAYS',
        y='WALLETS',
        title='Holders',
        color=px.Constant("DYDX Holders"),
        labels=dict(color="Holders")
    )
    figj.update_layout( hovermode='x unified')
    st.plotly_chart(
        figj,
        use_container_width=True
    )
with c2:
    figH = px.area(
        holders,
        x='DAYS',
        y='WALLETS_CUMULATIVE',
        title='Holders Cumulative',
        color=px.Constant("DYDX Holders"),
        labels=dict(color="Holders"))
    figH.update_layout( hovermode='x unified')
    st.plotly_chart(
        figH,
        use_container_width=True
    )

col1,col2= st.columns(2)
with col1:
    figp = px.pie(
        dist,
        values='WALLETS',
        names='DIST',
        title='DYDX Holders Distribution',
        hole=0.3
        )
    figp.update_layout( hovermode='x unified')
    st.plotly_chart(
        figp,
        use_container_width=True
    )
with col2:
    fig2 = px.bar(
        dist_overtime,
        x='DAYS',
        y='WALLETS',
        color='DIST',
        title='DYDX Holders last 120 days'
    )
    fig2.update_layout( hovermode='x unified')
    st.plotly_chart(
        fig2,
        use_container_width=True
    )
st.write('''
An analysis of DYDX holders shows that :red[21.1%] of them hold a very small amount of tokens, specifically between :blue[0 and 0.1] tokens, which is considered to be equivalent to having no tokens at all. Additionally, a further :red[5.65%] of DYDX holders possess less than :blue[1] token. This highlights the distribution of token ownership among DYDX holders with a significant portion of them holding minimal amounts of tokens.  

---
''')

h1,h2,h3,h4,h5 = st.columns(5)
with h1:
    st.metric('Holders under 0.1 DYDX',current_hold['HOLDER1'])
with h2:
    st.metric('Holders between 0.1 and 1 DYDx', current_hold['HOLDER2'])
with h3:
    st.metric('Holders between 1 and 10 DYDXs',current_hold['HOLDER3'])
with h4:
    st.metric('All Holders of DYDX',current_hold['TTL'])
with h5:
    st.metric('Actual Holders excluded less then 1 DYDX', current_hold['TTL']-current_hold['HOLDER1']-current_hold['HOLDER2'])

st.markdown('''
---


### Staking & Unstaking of dYdX

Staking refers to the process of locking up tokens in a contract in order to receive rewards or benefits. These rewards can include things like interest, governance rights, or access to exclusive features. Unstaking refers to the process of withdrawing tokens from a staked position and making them available for use or transfer again.


''')

g1,g2 = st.columns(2)
with g1:
    fig = px.bar(
        stak,
        x='DAYS',
        y='AMOUNT',
        color='TYPE',
        title='Staking amounts over last 90 days'
    )
    fig.update_layout( hovermode='x unified')
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
with g2:
    fig = px.bar(
        stak,
        x='DAYS',
        y='TXS',
        color='TYPE',
        title='Staking transactions over last 90 days'
    )
    fig.update_layout( hovermode='x unified')
    st.plotly_chart(
        fig,
        use_container_width=True
    )



st.markdown('''
---

### Transfers

As the charts shows the majority of DYDX tokens that are being transferred or being sent to centralized exchanges. Binance is a popular centralized exchange, and it is possible that a significant number of DYDX tokens are being transferred there in order to be sold on the platform.
''')

j1,j2 = st.columns(2)
with j1:
    fig = px.bar(
        cex,
        x='DAYS',
        y='TXS',
        title='Transactions toward CEXs',
        color='LABEL'
    )
    fig.update_layout( hovermode='x unified')
    st.plotly_chart(
        fig,
        use_container_width=True
    )
with j2:
    fig = px.bar(
        cex,
        x='DAYS',
        y='AMOUNTS',
        title='Amounts toward CEXs',
        color='LABEL'
    )
    fig.update_layout( hovermode='x unified')
    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown('''
---

### Swap

A swap refers to the process of exchanging one cryptocurrency for another. In the context of decentralized exchanges, a swap is typically conducted using smart contracts, which allow users to trade cryptocurrencies without the need for a central intermediary.

It is possible that the majority of DYDX tokens are being swapped to Wrapped Ethereum (WETH) or other stablecoins in decentralized exchanges. 
''')

y1,y2 = st.columns(2)
with y1:
    fimg = px.bar(
        swaps,
        x='DAYS',
        y='SWAPS',
        color='TOKEN_OUT',
        title='Swaps for tokens'
    )
    fimg.update_layout( hovermode='x unified')
    st.plotly_chart(
        fimg,
        use_container_width=True
    )
with y2:
    fim = px.bar(
        swaps,
        x='DAYS',
        y='AMOUNT',
        color='TOKEN_OUT',
        title='Swap Volume for (USD)'
    )

    fim.update_layout( hovermode='x unified')
    st.plotly_chart(
        fim,
        use_container_width=True
    )

st.markdown('''
---

### Conclusion

To wrap up, we see there is significant price drop due to market situations in recent months. In swapping pairs most of users prefer WETH to swap their dYdX token. Majority of holders are small holders which means they are holding less than 1000 dYdX tokens, and this small holders are increasing in recent days. In terms of staking we don't see any noticible change in staking amount and transactions although the unlocking has been postponed.
''')

u1,u2,u3,u4,u5 = st.columns((5))
with u1:
    st.info('Data Analysis by [[ Janan ](https://twitter.com/0x_janan)]',icon="✏️")
with u2:
    st.info('Source [[ Github ](https://github.com/0xjanan)]',icon="🖥")
with u3:
    st.info('Data from [[ Flipside Crypto ](https://flipsidecrypto.com)]',icon="🧠")
with u4:
    st.info('API from [[ Coingecko ](https://coingecko.com)]',icon="🏗")
with u5:
    st.info('Bounty from [[ MetricsDAO ](https://metricsdao.xyz)]',icon="🚇")

with st.expander('SQL sources'):
    st.write('''
        **This dashboard's charts are updating every 24 hours, so the numbers and percentages included in paragraphs may not be identical as the numbers showing on charts. The correct data will be shown on charts..**
        
        - https://app.flipsidecrypto.com/velocity/queries/ecca7d16-3ed5-4870-8229-6fe44350ece5
        - https://app.flipsidecrypto.com/velocity/queries/de06666e-ca1a-4939-a3d7-38acd0462f26
        - https://app.flipsidecrypto.com/velocity/queries/c9eec574-ed11-41a0-8187-47225293cf8c
        - https://app.flipsidecrypto.com/velocity/queries/6e18b3e0-3128-4c9f-88e5-86e3250651a2
        - https://app.flipsidecrypto.com/velocity/queries/6b34034b-752b-4414-baec-1f89320290e9
        - https://app.flipsidecrypto.com/velocity/queries/1d54d4a6-9aac-4de6-9871-aecb4c469ac2
        - https://app.flipsidecrypto.com/velocity/queries/c221f673-4f2a-4cd9-b58a-0e64e51a2c14
        - https://app.flipsidecrypto.com/velocity/queries/a845a423-9049-4251-ab47-f83b0abe6fe4
    ''')
