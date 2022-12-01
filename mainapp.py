import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import drinkcalculations  # Import do trigger a file run <- But you might want to run it a at differnet moment
from PIL import Image
from random import choices, randint

# GLOBAL LEVEL CODE
global drinkPrice
drinkPrice = 0

# does dataset for names need to be saved

if 'calculatedCost' not in st.session_state:
    st.session_state['calculatedCost'] = False
if 'calculatedCostCorrectly' not in st.session_state:
    st.session_state['calculatedCostCorrectly'] = False

st.set_page_config(
    page_title="Scientific Drinking",
    page_icon=":tophat:",
    layout="wide",
)

# NAME GENERATOR

if 'nameSet' not in st.session_state:
    st.session_state['nameSet'] = {"format 1": ([
                                                    # "Tsar",
                                                    "Dynamo",
                                                    "Bloody",
                                                    "Dirty",
                                                    "Blue",
                                                    "Fat",
                                                    "Biggus",
                                                    "Banzai",
                                                    "Charming",
                                                    "Raging"

                                                ], ["Bomba",
                                                    "Keops",
                                                    "Man",
                                                    "Russian",
                                                    "Tsar",
                                                    "Lagoon",
                                                    "Virgin",
                                                    "Napoleon",
                                                    "Kremlin",
                                                    "Bro",
                                                    "Consul",
                                                    "Prussian",
                                                    "Revolution"
                                                    ]),

        "format 2": (["Butler’s",
                      "Tsar’s",
                      "Zelenskyi’s",
                      "Agent’s",
                      ], ["Kick",
                          "Paradise",
                          "Sea Grape",
                          "Winter Melon",
                          "Elixir",
                          "Fist"
                          ]),

        "Unique Names": ["Tsar Bomba",
                         "Little Boy",
                         "Fat Man",
                         "Pistol Star",
                         "007",
                         "Keops Pyramid",
                         "Industrial Revolution"
                         ]}


def randomGen(lst):
    keys = list(st.session_state["nameSet"].keys())
    path = ""
    # WHICH BARREL TO SCRAPE
    if len(keys) == 3:
        path = choices(keys, weights=[55, 30, 15], k=1)[0]
    elif len(keys) == 2:
        path = choices(keys, weights=[35, 65], k=1)[0]
    elif len(keys) == 1:
        path = choices(keys, k=1)[0]
    else:
        return "Out of Name Ideas"

    if path == "Unique Names":
        name = st.session_state["nameSet"][path][randint(0, len(st.session_state["nameSet"][path]) - 1)]
        st.session_state["nameSet"][path].remove(name)
        if len(st.session_state["nameSet"][path]) == 0:
            del st.session_state["nameSet"][path]
            return name
        else:
            return name
    else:

        def wordGen(poolFormat, name, iLimit):
            i = 0
            triedWords = {}
            while name in lst and i < iLimit:  # problematic that it tries the same combinations again. Guessing the word that we have already guessed.
                firstPart = st.session_state["nameSet"][poolFormat][0][
                    randint(0, len(st.session_state["nameSet"][poolFormat][0]) - 1)]
                secondPart = st.session_state["nameSet"][poolFormat][1][
                    randint(0, len(st.session_state["nameSet"][poolFormat][1]) - 1)]
                name = f"{firstPart} {secondPart}"

                if name in triedWords:
                    continue
                else:
                    triedWords[name] = 1
                    i += 1
            if i == iLimit:
                return "", False  # didn't find a new combination
            else:
                return name, True

        name = ""  # "default". Makes it so that the while loop runs at least once
        iLimit = 24
        if path == "format 1":
            iLimit = 117

        retVal = wordGen(path, name, iLimit)
        if not retVal[1]:
            del st.session_state["nameSet"][path]
            return randomGen(lst)
        else:
            return retVal[0]


# -----------------------------------------------
# THE WEBISTE
# st.write("# Scientific Drinking - Know What You Drink")
st.image(Image.open("Drink Optimzer.png"))

with open("styling.css") as style:
    st.markdown(f"<style> {style.read()} </style>", unsafe_allow_html=True)

drinktab, yourlevel = st.tabs(["Make Your Drink", "Enjoy your drinks"])

with drinktab:
    # INPUT WIDGETS
    st.write("**Notice:** This site promotes safe (and fun!) drinking and aims to reduce overdrinking. "
             "Our goal is to make people aware how different drinks might affect them.")
    st.write("### Your special mix:")
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")
    with col1:
        nonAlcoholAmount = st.number_input("Non-Alcoholic mixer amount in liters", min_value=0.0, step=0.5,
                                           format="%.2f", value=0.5)
    with col2:
        alcoholAmount = st.number_input("Alcoholic drink amount in liters", min_value=0.0, step=0.5, format="%.2f",
                                        value=0.33)
    with col3:
        alcoholPercentage = st.number_input("Alcohol percentage %", min_value=0.0, step=5.0, format="%.2f",
                                            help="An input of 26,7 indicates 26.7%. Not 0.267 != 26.7%", value=20.0)

    # GLOBAL VARIABLES TO HELP WITH THE COLUMNS BELOW
    volume, level, emptySpace = st.columns([1, 1, 5], gap="small")
    totalVolume = nonAlcoholAmount + alcoholAmount

    # METRICS
    with volume:
        if 'lastTotalVolume' not in st.session_state:
            st.metric("Drink Volume Liters", f"{round(totalVolume, 2)}L")
            st.session_state['lastTotalVolume'] = totalVolume
        else:
            st.metric("Drink Volume Liters", f"{round(totalVolume, 2)}L",
                      delta=str(round(totalVolume - st.session_state.lastTotalVolume, 2)) + "L")

            st.session_state['lastTotalVolume'] = totalVolume
    with level:
        if totalVolume > 0:
            if 'alcoholLevel' not in st.session_state:  #
                calculatingPercentage = alcoholPercentage / 100
                alcoholLevel = ((alcoholAmount * calculatingPercentage) / totalVolume) * 100
                st.metric("Alcohol Level % ",
                          str(round(alcoholLevel, 2)) + "%")
                st.session_state['alcoholLevel'] = alcoholLevel
            else:
                calculatingPercentage = alcoholPercentage / 100
                alcoholLevel = ((alcoholAmount * calculatingPercentage) / totalVolume) * 100

                # GETTING A DASH WHEN 0 - CASE WHEN YOU DECREASE THE ALCOHOL LEVEL AND THE ALCOHOL AMOUNT IS 0L
                result = round(alcoholLevel - st.session_state.alcoholLevel, 2)
                if result == 0:
                    result = None
                    st.metric("Alcohol Level % ", str(round(alcoholLevel, 2)) + "%",
                              delta=result)
                else:
                    st.metric("Alcohol Level % ",
                              str(round(alcoholLevel, 2)) + "%",
                              delta=str(result) + " %-Unit")
                    st.session_state.alcoholLevel = alcoholLevel
        else:
            st.metric("Alcohol Level % ", '0.0%')

    chart, drinkprice = st.columns(2, gap="small")

    # CHART DISPLAY

    # DRINK THIS DRINK

    with chart:
        if alcoholAmount > 0 and alcoholPercentage > 0:  # SHOW THE CHART ONLY WHEN THESE INPUTS ARE GIVEN

            # PREPARING THE DATA FOR THE CHART
            alcoholCombinations = np.linspace(0, alcoholAmount * 2, 110)

            df = pd.DataFrame(alcoholCombinations, columns=['Alcoholic Drink Amount (Liters)'])

            df['Total Volume (Liters)'] = df['Alcoholic Drink Amount (Liters)'] + nonAlcoholAmount
            df["Alcohol % level"] = (
                    (df['Alcoholic Drink Amount (Liters)'] * calculatingPercentage) / df['Total Volume (Liters)'])

            df.reset_index(drop=True, inplace=True)

            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df["Alcoholic Drink Amount (Liters)"], y=df["Alcohol % level"],
                                     line=dict(color="#FF5A91"),
                                     customdata=df["Total Volume (Liters)"],
                                     name="",
                                     hovertemplate="<b>Alcohol Level: %{y:.2%}</b> <br></br>" + "Alcoholic Drink Amount<b>:</b> %{x:.2f}L<br>" + "Total Volume<b>:</b> %{customdata:.2f}L"
                                     ))

            fig.update_layout(
                title={'text': "Alcohol Combinations", 'y': 0.964, 'yanchor': 'top', 'font': dict(size=20)},

                yaxis=go.layout.YAxis(tickformat=".1%", rangemode="tozero", gridcolor="#4F4A55",
                                      gridwidth=1,
                                      ticksuffix="  ", mirror=True,
                                      title=dict(font=dict(size=17),
                                                 text="Alcohol % level", standoff=15), showspikes=True,
                                      spikethickness=2, spikecolor="#6F637E",
                                      tickfont=dict(size=15), ticklabeloverflow='hide past div'
                                      ),
                xaxis=go.layout.XAxis(tickformat=".2",
                                      tickmode="array", ticklabelposition="outside",
                                      showgrid=False, mirror=True, nticks=5,
                                      title=dict(font=dict(size=17),
                                                 text="Alcoholic Drink Amount (Liters)",
                                                 standoff=15), showspikes=True, spikethickness=2,
                                      spikecolor="#6F637E", tickfont=dict(size=15),  #
                                      rangeslider=dict(visible=True, bordercolor="#6D6969", borderwidth=1)),
                plot_bgcolor="#202225",
                hoverlabel=dict(bgcolor="#202225", font=dict(color="#E3E2E2"), bordercolor="#4F4A55"),
                margin=dict(t=53), modebar=dict(remove=["zoom", "resetscale", "pan", "zoomin", "zoomout", ], ))

            # chart must be alingnd properly
            # chart positioning

            st.plotly_chart(fig, use_container_width=True)

        else:
            defaultFig = go.Figure()
            defaultFig.update_layout(
                title={'text': "Alcohol Combinations", 'y': 0.964, 'yanchor': 'top', 'font': dict(size=20)},
                xaxis=dict(showgrid=False, rangemode="tozero",
                           title=dict(font=dict(size=17), text="Alcoholic Drink Amount (Liters)")),
                yaxis=dict(rangemode="tozero", title=dict(font=dict(size=17), text="Alcohol % level", standoff=15),
                           showgrid=False),
                modebar=dict(remove=["zoom", "resetscale", "pan", "zoomin", "zoomout"]),
                annotations=[
                    go.layout.Annotation(text="No Data", xref="paper", yref="paper", y=0.5, x=0.5, showarrow=False,
                                         opacity=0.6,
                                         font=dict(size=35), )]

            )

            st.plotly_chart(defaultFig, use_container_width=True)

        # INITIALIZING THE TABLE AND SAVING IT TO STATE

        tableCols = ["Name", "Volume", "Alcohol level", "Time", "Price"]
        if "drinkTable" not in st.session_state:
            st.session_state["drinkTable"] = pd.DataFrame(columns=tableCols)

        with drinkprice:
            st.write(
                "#### Your Drink's Price")  # equals to x amount of olut beer, so theres the perspecitve! liköörpullo vastaa noin viittä lidl olutta vain"
            with st.form(key="pricedata"):
                st.write("The prices of your ingredients: ")
                amountBought = st.number_input("Non-Alcohol amount bought: (Liters)", min_value=0.0, step=0.5,
                                               format="%.2f")
                pricePerAmount = st.number_input("Price €: ", min_value=0.0, step=0.5, format="%.2f",
                                                 key="nonalcoholprice")
                alcoholAmountBought = st.number_input("Alcohol amount bought: (Liters)", min_value=0.0, step=0.5,
                                                      format="%.2f", value=0.33)
                pricePerAlcoholAmount = st.number_input("Price €: ", min_value=0.0, step=0.5, format="%.2f",
                                                        key="alcoholprice", value=0.99)

                response = st.form_submit_button('Calculate')  # aina kun painaa niin muuttu falseksi.
                if response:
                    st.session_state['calculatedCost'] = True

    whiteSpace, costAnalysis = st.columns(2)

    if st.session_state['calculatedCost']:
        if alcoholAmount > 0 and nonAlcoholAmount > 0 and alcoholAmountBought > 0 and amountBought > 0:
            with costAnalysis:
                st.write("### Calculated Cost Analysis :bar_chart:")
                st.write("---")
                drinkPrice, print = drinkcalculations.bothProvided(amountBought, pricePerAmount, alcoholAmountBought,
                                                                   pricePerAlcoholAmount,
                                                                   alcoholAmount, nonAlcoholAmount,
                                                                   calculatingPercentage)
                st.session_state['calculatedCostCorrectly'] = True
                st.write(print)
        elif alcoholAmount > 0 and alcoholAmountBought > 0 and nonAlcoholAmount == 0:
            with costAnalysis:
                st.write("### Calculated Cost Analysis :bar_chart:")
                st.write("---")
                drinkPrice, print = drinkcalculations.onlyAlcohol(alcoholAmount, pricePerAlcoholAmount,
                                                                  calculatingPercentage,
                                                                  alcoholAmountBought)
                st.session_state['calculatedCostCorrectly'] = True
                st.write(print)
        elif alcoholAmount <= 0:
            with costAnalysis:
                st.write("### Calculated Cost Analysis :bar_chart:")
                st.write("---")
                st.write("I agree, Alcohol is bad for you. Better stay away from it.")
                st.session_state['calculatedCostCorrectly'] = False  # makes it so you cant drink non-alcoholic drinks
        elif alcoholAmount > 0 and alcoholAmountBought == 0:
            with costAnalysis:
                st.write("### Calculated Cost Analysis :bar_chart:")
                st.write("---")
                st.write("Enter the stats of the alcohol constituent.")
                st.session_state['calculatedCostCorrectly'] = False
        elif nonAlcoholAmount > 0 and amountBought == 0:
            with costAnalysis:
                st.write("### Calculated Cost Analysis :bar_chart:")
                st.write("---")
                st.write("Enter the stats of the non-alcohol constituent.")
                st.session_state['calculatedCostCorrectly'] = False
        elif alcoholAmountBought <= 0 and amountBought <= 0:
            with costAnalysis:
                st.write("### Calculated Cost Analysis :bar_chart:")
                st.write("---")
                st.write("O-oops! You forgot to enter your ingredient stats!")
                st.session_state['calculatedCostCorrectly'] = False
    else:
        with costAnalysis:
            st.write("### Calculated Cost Analysis :bar_chart:")
            st.write("---")

    with yourlevel:
        # DRINKING BUTTON
        if alcoholAmount > 0 and alcoholLevel > 0:
            st.write(f"The selected drink contains: **{round(alcoholLevel, 2)}%** alcohol and "
                     f"it has a total volume of **{round(alcoholAmount + nonAlcoholAmount, 2)} Liter(s)**")
            drinkTimeWidget, margin = st.columns([1, 2])
            with drinkTimeWidget:
                drinkTime = st.number_input("Estimated time to drink: (In minutes)", min_value=0, step=5)


            def addToTable(nonAlcoholAmount, alcoholAmount, alcoholLevel, drinkTime, drinkPrice):
                sumVolume = nonAlcoholAmount + alcoholAmount
                drinkName = ""
                indexOfSameDrink = st.session_state["drinkTable"].index[
                    (st.session_state["drinkTable"]["Volume"] == sumVolume)
                    & (st.session_state["drinkTable"]["Price"] == drinkPrice)
                    & (st.session_state["drinkTable"]["Alcohol level"] == alcoholLevel)].tolist()
                if len(indexOfSameDrink) > 0:
                    drinkName = st.session_state["drinkTable"].iloc[indexOfSameDrink[0], 0]
                else:
                    lstForGenerator = list(st.session_state["drinkTable"]["Name"].append(pd.Series([""]),
                                                                                         ignore_index=True))
                    drinkName = randomGen(lstForGenerator)

                st.session_state["drinkTable"] = pd.concat(
                    [st.session_state["drinkTable"],
                     pd.Series(
                         {"Name": drinkName, "Volume": sumVolume, "Alcohol level": alcoholLevel,
                          "Time": drinkTime, "Price": drinkPrice}).to_frame().T]
                    , ignore_index=True)


            def errorMsgForAddToTable():
                st.write(
                    "Oh OH! You need to insert the drinking time and calculate the drink's price on the (Make your "
                    "drink - tab) before pressing me!")

                # BEFORE PRESSING; TIME AND PRICE NEED TO BE SET


            if drinkTime > 0 and st.session_state['calculatedCostCorrectly']:
                if st.button("Drink Your artwork"):
                    addToTable(nonAlcoholAmount, alcoholAmount, alcoholLevel, drinkTime, drinkPrice)
            else:
                if st.button("Drink your artwork."):
                    errorMsgForAddToTable()

        else:
            "Waiting for your special mix... Make your drink by using the on the "
            drinkTimeWidget, margin = st.columns([1, 2])
            with drinkTimeWidget:
                drinkTime = st.number_input("Estimated time to drink: (In minutes)", min_value=0, step=5)
                st.button("Drink your artwork")

        # BUILDING UP THE DATAFRAME
        st.write("#### Beverages you've already consumed:")
        drinkingTime = st.session_state['drinkTable']['Time'].sum() / 60

        gender, weight, tableInterface = st.columns([1, 1.5, 5.1])  # PARAMS NEEDED FOR CALCULATING BAC
        with gender:
            r = 0.55
            genderParam = st.radio("Gender", ["Man", "Woman"], label_visibility="hidden", horizontal=True)
            if genderParam == "Man":
                r = 0.65
        with weight:
            weightParam = st.number_input("Weight (Kg)", min_value=0.0, step=5.0,
                                          help="Insert your weight to calculate your alcohol level") * 1000

        with tableInterface:
            if len(st.session_state['drinkTable']) >= 1:
                itemToDelete = st.selectbox(label="not needed",
                                            options=st.session_state["drinkTable"]["Name"].drop_duplicates(),
                                            label_visibility='hidden')
                if st.button("Delete item"):
                    rowToDelete = list(
                        st.session_state['drinkTable'][st.session_state['drinkTable']["Name"] == itemToDelete].index)[0]

                    st.session_state['drinkTable'].drop(rowToDelete, inplace=True)
                    st.session_state['drinkTable'].reset_index(inplace=True, drop=True)

        st.table(st.session_state["drinkTable"].style.format(
            {"Alcohol level": "{:.2f}%", "Volume": "{:.2f}L",
             "Time": "{:.0f} Minutes", "Price": "{:.2f}€"}), )
        # use_container_width=True)

        # index=pd.RangeIndex(start=1) & .loc[1:len(st.session_state["drinkTable"]),]
        st.write("---")
        left, price, bac, time, volume, right = st.columns([0.5, 1, 1, 1.9, 1, 0.5])
        bacLevel = 0
        with price:
            st.metric("Price:", value=f"{round(st.session_state['drinkTable']['Price'].sum(), 2)}€")
        with bac:
            if weightParam > 0:
                pureAlchol = (st.session_state['drinkTable']['Volume'] * (st.session_state['drinkTable'][
                    'Alcohol level']) / 100).sum()

                alcholInGrams = pureAlchol * 1000 * 0.7894
                bacLevel = round((alcholInGrams / (weightParam * r)) * 1000 - (drinkingTime * 0.15),
                                 2)  # Huomaa että palamisnopeus ei ollut promilleina!!!

                st.metric("Body Alcohol Level:", f"{bacLevel} \u2030")
        with time:
            minutes = st.session_state['drinkTable']['Time'].sum()
            if minutes >= 100:
                hours = int(minutes / 60)
                minutes = minutes % 60
                st.metric("Party time:", f"{hours} hours and {minutes} Minutes")
            else:
                st.metric("Party time:", f"{minutes} Minutes")
        with volume:
            st.metric("Liquid drank:", f"{round(st.session_state['drinkTable']['Volume'].sum(), 2)} Liters")

        st.write("---")
        st.write("#### State analysis: ")

        if 0 < bacLevel <= 0.29:
            st.write(":point_right: Average individual appears normal. Maybe a little more excited than usual.")
        elif 0.3 <= bacLevel < 0.59:
            st.write(
                ":heavy_check_mark: Mild euphoria kicks in. You feel relaxed... Yet Joyous.  \n:speech_balloon: You talk to strangers like you have known "
                "them for years.  \n:clinking_glasses: You feel like this in going to be a good night.")

        elif 0.6 <= bacLevel <= 0.99:
            st.markdown(":heavy_check_mark: High levels of euphoria.  \n"
                        ":man-cartwheeling: You occasionally lose your balance and you "
                        "struggle to keep "
                     "yourself up."
                     "... Which causes funny moments.  \n"
                     ":scales: Alcohol clouds your judgement and perceived risks decrease.  \n"
                     ":family: You seek contact with other humans through cuddling, dancing or fighting.  \n"
                     ":point_right: You shouldn't drink any more though.")
        elif 1.0 <= bacLevel <= 2.0:
            st.write(":dizzy: Now walking and physical tasks get harder.. Big time.  \n:face_vomiting: The state of "
                     "euphoria is replaced by "
                     "the "
                     "feeling of nausea. You start vomiting.  \n:speech_balloon: Your mouth says whatever it wants.  \n"
                     ":x: You've crossed the line.  \n"
                     ":point_right: Better get some rest and drink water.")
        elif bacLevel > 2.00:
            st.write(":face_vomiting: Nausea and vomiting continues...  \n"
                     ":x: Total mental confusion and memory blackout.  \n"
                     ":point_right: Seek help, or you better start looking for a tombstone.")
        else:
            st.write(":heavy_check_mark: You are sober. ")
