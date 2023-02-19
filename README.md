# Blaze Double - Study
**This project is part of a friend challenge.**

I have a friend, who I will call as Will, that bets on Blaze. Will told me that he detected sine patterns in the draws on that site and that **he won US$4,000** in October/22. I said "Ok, let's check it out, I'll try to predict the draws and we'll see if it is really random or has some patterns as you say" and then this project came to life.

This project is split in 2 Blaze's Products:
* Double - the main Blaze's product
* Crash  - a "new" product

## How Double work?
**Double has 15 numbers from 0 to 14.** If the number draw is 0, the person who bet on color White wins 14x what he bet. If the number draw is 1 up to 7, the person who bet on color Red wins 2x what he bet. If the number draw is above 7, the person who bet on color Black wins 2x what he bet.

* **White** Color: number 0
* **Red** Color: number 1-7
* **Black** Color: number 8-14

So we have 46.67% chance of getting red color, 46.67% chance of getting black color and 6.67% of getting white color in any draw.

We will try to predict these 3 colors using **Classifiction models**. After that, we will try to predict only the White color - the most profitable color.

---
You can find the notebooks for study in the folder "Double" and the data in "Double_data". There's no other folder because this project is only for study and part of a challenge.