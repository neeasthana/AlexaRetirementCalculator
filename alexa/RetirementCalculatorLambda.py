"""
Lambda function handler for Retirement Calculator Alexa skill
"""

from __future__ import print_function
import random




# --------------- ROUTERS ------------------ #

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])



def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "CalculateRetirementTime":
        return calculate_retirement_time(intent_request, session)
    elif intent_name == "Disclaimer":
        return get_disclaimer(intent_request, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")



# --------------- WELCOME AND ENDING HANDLERS ------------------ #



def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # Dispatch to your skill's launch
    return get_welcome_response()

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


def get_welcome_response():
    """
    Welcome message when you open the Retirement Calculator Skill
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Retirement Calculator. We can help you estimate how long it will take you to retire based on your current financial situation."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with the same text.
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    """
    Closing message when you end the Retirement Calculator Skill
    """
    card_title = "Session Ended"
    speech_output = "Thank you for using the Retirement Calculator skill!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_help_response():
    """
    Help message when you ask for assistance
    """
    session_attributes = {}
    card_title = "Help"
    speech_output = "We can help you estimate how long it will take you to retire based on your current financial situation. A couple of examples of questions that I can help with are... What is the coding dojo... or, who are the instructors. Lets get started now by trying one of these."

    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))



# --------------- RESPONSE BUILDERS ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }



def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def build_response2(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response


def continue_dialog(session_attributes):
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    return build_response2(message, session_attributes)



# --------------- RETIREMENT FACTS ------------------ #



def random_fact():
    """
    random retirement statistics
    """
    facts = [
          "At the time of retirement the average four oh one k has one hundred thousand dollars"
        , "Start saving and investing early"
        , "Use low fees index funds"
        , "the time value of money"
        , "the rule of 72 is a simple trick to estimate how quickly you can double your money. Just take the percentage of your investment return which is on average 7 percent in the stock market and do 72 divided by that number. So by this estimation the stock market will approximately double every 10 years"
    ]
    return facts[random.randint(0,len(facts)-1)]



# --------------- RETIREMENT MATH ------------------ #



def _money_at_retirement(age, monthly_savings, monthly_spend, savings, investment_return = 1.06, inflation = 1.02):
    """
    recursive function to obtain the amount of money you will have after one year
    """
    new_savings = (savings * investment_return) + (12*monthly_savings)
    new_age = age + 1
    new_monthly_spend = monthly_spend * inflation
    new_monthly_savings = monthly_savings * inflation

    return new_age, new_savings, new_monthly_savings, new_monthly_spend

    # return _money_at_retirement(new_age, new_monthly_savings, new_monthly_spend, new_savings, retirement_age, investment_return)


   
def _money_through_retirement(age, life_expectancy, savings, inflation, investment_return):
    """
    function to find how much money you can spend monthly/yearly during your retirement
    exponent = age - life_expectancy
    savings/exponent * (1 + investment_return)^exponent 
    """
    exponent = life_expectancy - age
    yearly_spend = (savings / exponent) * ((1 + (investment_return- inflation)) ** exponent)
    yearly_spend_adjusted_retire_year = yearly_spend / (inflation ** exponent)
    return yearly_spend, yearly_spend/12, yearly_spend_adjusted_retire_year



def _retirement_time(age = 30, monthly_savings=0, monthly_spend=0, savings= 0, retirement_age = 65, life_expectancy = 95, investment_return = 1.06):
    
    result = {
        "time": 65 - age,
        "age": 65,
        "at_retirement": _money_at_retirement(age, monthly_savings, monthly_spend, savings, retirement_age, investment_return)
    }
    return result



def _age_till_retirement(age = 30, life_expectancy = 95, monthly_savings=0, monthly_spend=0, savings= 0, investment_return = 1.06, inflation = 1.02):
    latest_calculations = {
        "age": age,
        "time": age - age, 
        "savings_at_retirement": savings,
        "monthly_savings": monthly_savings,
        "monthly_spend": monthly_spend,
        "monthly_spend_through_retirement": 0,
        "yearly_spend_adjusted_retire_year": 0, 
        "monthly_spend_adjusted_retire_year": 0
    }

    # Iterate through current age to life expectancy
    for i in range(age, life_expectancy):
        # money if they retire at this age
        new_age, new_savings, new_monthly_savings, new_monthly_spend = _money_at_retirement(i, latest_calculations["monthly_savings"], latest_calculations["monthly_spend"], latest_calculations["savings_at_retirement"], investment_return, inflation)

        # money through retirement
        yearly_spend, retirement_monthly_spend, yearly_spend_adjusted_retire_year = _money_through_retirement(i, life_expectancy, new_savings, inflation, investment_return - .02)



        print(yearly_spend_adjusted_retire_year/12, new_monthly_spend)

        latest_calculations = {
            "age": new_age,
            "time": new_age - age, 
            "savings_at_retirement": new_savings, # how much money you will have at the end of the year for your retirement (or at the end of the year if calculations are not done)
            "monthly_savings": new_monthly_savings, # money saved every month after being adjusted for inflation
            "monthly_spend": new_monthly_spend, # money spent every month after being adjusted for inflation
            "monthly_spend_through_retirement": retirement_monthly_spend, # money that can be spent monthly through retirement (without inflation adjustment for retirement year)
            "yearly_spend_adjusted_retire_year": yearly_spend_adjusted_retire_year, # money that can be spent yearly through retirement (with inflation adjustment for retirement year)
            "monthly_spend_adjusted_retire_year": yearly_spend_adjusted_retire_year/12 # money that can be spent monthly through retirement (with inflation adjustment for retirement year)
        }

        # Check to see if the adjusted for inflation retirement monthly spend is greater than the current monthly spend implying that you can retire now and still survive till your life expectancy
        if yearly_spend_adjusted_retire_year/12 >= new_monthly_spend:
            break
    return latest_calculations



# --------------- CUSTOM INTENT HANDLERS ------------------ #


# Example intent_request: 
# {'type': 'IntentRequest', 
#  'requestId': 'amzn1.echo-api.request.4390e9d3-974a-47db-9596-ae9c59e141cd', 
#  'timestamp': '2018-10-01T19:31:41Z', 
#  'locale': 'en-US', 
#  'intent': {
#       'name': 'CalculateRetirementTime', 
#       'confirmationStatus': 'NONE', 
#       'slots': {
#           'Savings': {'name': 'Savings', 'value': '200000', 'confirmationStatus': 'NONE'}, 
#           'Monthly_Savings': {'name': 'Monthly_Savings', 'value': '2000', 'confirmationStatus': 'NONE'}, 
#           'Avg_Monthly_Spending': {'name': 'Avg_Monthly_Spending', 'value': '3000', 'confirmationStatus': 'NONE'}, 
#           'Age': {'name': 'Age', 'value': '55', 'confirmationStatus': 'NONE'}}}, 
#  'dialogState': 'COMPLETED'}
def calculate_retirement_time(intent_request, session):
    dialog_state = intent_request['dialogState']
    intent = intent_request['intent']

    session_attributes = {}
    if session and "attributes" in session:
        session_attributes  = session["attributes"]
    card_title = "Calculate_Retirement_Time"

    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog(session_attributes)

    elif dialog_state == "COMPLETED":
        age = int(intent['slots']['Age']['value'])
        monthly_savings = float(intent['slots']['Monthly_Savings']['value'])
        monthly_spend = float(intent['slots']['Avg_Monthly_Spending']['value'])
        savings = int(intent['slots']['Savings']['value'])

        retirement_calculations = _retirement_time(age, monthly_savings, monthly_spend, savings)

        _age_till_retirement = _age_till_retirement(age = age, monthly_savings=monthly_savings, monthly_spend=monthly_spend, savings= savings)

        session_attributes = {
            "age": age,
            "monthly_savings": monthly_savings,
            "monthly_spend": monthly_spend,
            "savings": savings,
            "retirement_info": retirement_calculations
        }

        speech_output = ("Based on your current financial picture and savings habits we estimate that you will be able to retire in " + str(retirement_calculations["time"]) + " years. " 
            "At this time you will be " + str(retirement_calculations["age"]) + " and we estimate you will have " + str(retirement_calculations['savings_at_retirement']) + " dollars saved after adjusting for 2 percent yearly inflation and investment returns of 6 percent annually. "
            "During retirement you should be able to spend about " + str(retirement_calculations['monthly_spend_through_retirement']) + " dollars every month")

        reprompt_text = speech_output
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

    else:
        return statement("Calculate_Retirement_Time", "No dialog")


def get_disclaimer(intent_request, session):
    """
    Financial Disclaimer for using this retirement calculator
    """
    session_attributes = {}
    if session and "attributes" in session:
        session_attributes  = session["attributes"]
    speech_output = "These calculations are hypothetical and do not represent the return on any particular investment. All investing is subject to risk, including the possible loss of the money you invest. The calculations provided serve as an estimate and are meant to be informative and will not accurately predict each situation."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

if __name__ == '__main__':
    intent_request = {'type': 'IntentRequest', 'requestId': 'amzn1.echo-api.request.4390e9d3-974a-47db-9596-ae9c59e141cd', 'timestamp': '2018-10-01T19:31:41Z', 'locale': 'en-US', 'intent': {'name': 'CalculateRetirementTime', 'confirmationStatus': 'NONE', 'slots': {'Savings': {'name': 'Savings', 'value': '200000', 'confirmationStatus': 'NONE'}, 'Monthly_Savings': {'name': 'Monthly_Savings', 'value': '2000', 'confirmationStatus': 'NONE'}, 'Avg_Monthly_Spending': {'name': 'Avg_Monthly_Spending', 'value': '3000', 'confirmationStatus': 'NONE'}, 'Age': {'name': 'Age', 'value': '55', 'confirmationStatus': 'NONE'}}}, 'dialogState': 'COMPLETED'}
    # print(calculate_retirement_time(intent_request, None))

    # print(retirement_age(65, 95, 300000, .02, .05))

    print(_age_till_retirement(age = 30, life_expectancy = 95, monthly_savings=3000, monthly_spend=3000, savings= 100000, investment_return = 1.06, inflation = 1.02))