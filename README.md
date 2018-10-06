# AlexaRetirementCalculator
An Alexa Skill to help users estimate their time to retirement by asking questions about their current and future financial situations. 

The Retirement skill will also provide basic financial advice to help users reach their financial and retirement goals.

## Usage

To open the skill say...

'''
Alexa, open retirement calculator
	>> Welcome to the Alexa Retirement Calculator...
'''

Ask questions like:

'''
How long till I can retire?
'''

## Repository Contents

- '/alexa' - necessary files for the Alexa Skill
	- 'RetirementCalculatorLambda' - Lambda function that serves as the backend handler (written in python)
	- 'interaction-model.json' - Interaction model for Skill including all Intents and Sample Utterances
- 'README.md'

## Future features

1. Incorporate additional options for getting a better picture of retirement including:
	- debt
	- length of debt
	- mortgages
	- social security
	- yearly investment return % change
	- college payments for kids
	- having kids
	- life expectancy
	- inflation rate
	- taxes
	- expected retirement costs

1. Tips to speed up retirement
	- increase monthly savings
	- utilizing a 401(k) or IRAs 
	- decrease spending every month to save more
	- financial advisors

1. Incorporation of averages and target for the US based on age

1. Disclaimer intent

1. Different age for retirement after getting your retirement calculations for 65 (use session_attributes to store for every age)

## References

Retirement Calculator Math
	- https://outgrow.co/blog/retirement-calculator
	- https://www.wikihow.com/Calculate-Amount-Needed-for-Retirement

## Contact

If you would like to contact the developer or provide any feedback please feel free to email me at 'neeasthana@gmail.com'

Thank you for all of your support!

