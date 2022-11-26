def bothProvided(nonAlcoholAmountBought, pricePerNonAlcoholAmount, alcoholAmountBought, pricePerAlcoholAmount,
                 alcoholAmount,
                 nonAlcoholAmount, calculatingPercentage):
    litrePriceForNonAlcohol = (1 / nonAlcoholAmountBought) * pricePerNonAlcoholAmount

    litrePriceForAlcohol = (1 / alcoholAmountBought) * pricePerAlcoholAmount

    totalcost = round(alcoholAmount * litrePriceForAlcohol + nonAlcoholAmount * litrePriceForNonAlcohol,
                      2)

    purealcohol = alcoholAmount * calculatingPercentage
    pureAlcoholInOneBeer = 0.33 * 0.045
    olutBeers = round(purealcohol / pureAlcoholInOneBeer, 2)

    # better analysis an explain that the vlaue of the input widgets are used not the values inputted in the form.
    return totalcost, f"- The drink costs **{totalcost}€** and is equivalent to **{olutBeers}** Olut-beers. " \
                      f"The price difference is {round(olutBeers - totalcost, 2)}€." \
                      f"(A negative value means that it would be cheaper to get the same alcohol amount with Olut-beers. " \
                      f"If the difference is positive, your drink is cheaper."



def onlyAlcohol(alcoholAmount, pricePerAlcoholAmount, alcoholPercentage, alcoholAmountBought):
    litrePriceForAlcohol = (1 / alcoholAmountBought) * pricePerAlcoholAmount
    totalPrice = alcoholAmount * litrePriceForAlcohol

    pureAlcoholInOneBeer = 0.33 * 0.045

    purAlcoholInDrink = alcoholAmount * alcoholPercentage
    olutBeers = round(purAlcoholInDrink / pureAlcoholInOneBeer, 2)

    return totalPrice, f"The drink costs **{round(totalPrice, 2)}€** and is equivalent to **{olutBeers}** Olut-beers. The price difference is {round(olutBeers - totalPrice, 2)}€.\n " \
           f"(A negative value means that it would be cheaper to get the same alcohol amount with Olut-beers. " \
           f"If the difference is positive, your drink is cheaper."
