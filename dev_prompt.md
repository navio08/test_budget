## To Do 
- [x] Use case scoping
- [x] Basic prompt scoping
  - [x] Add notes
  - [x] Prompt 01: Initial educated guess
    - [x] Compare with insta post & OpenAI startup resource
    - [x] Save results of the current prompt - change the code to log the prompt to a log file. Add the log file to .gitignore
    - [x] Sanity check of the first version
- [ ] [Prompt 02: Use OpenAI API](https://platform.openai.com/docs/guides/text?api-mode=responses). Goal: Use a more efficient library for prompting:
  - [x] Quick tutorial of the OpenAI API (15-30min video on YT)
    - [x] Clarify concepts: tokens usage, completiion, total, roles (system vs user), etc.
  - [ ] Adapt the prompt for ChatGPT-5 & test: 
    - [ ] [Switch to response](https://platform.openai.com/docs/api-reference/responses/create)
    - [ ] [Instructions API](https://platform.openai.com/docs/guides/text?api-mode=responses&lang=python#message-roles-and-instruction-following): Use developer/user roles. The user will just feed the input parameters. 
    - [ ] [Reusable prompts (for prod)](https://platform.openai.com/docs/guides/text?api-mode=responses&lang=python#reusable-prompts)
    - [ ] [Structured output (for prod)](https://platform.openai.com/docs/guides/structured-outputs)
    - [ ] [Model evaluation (before going into prod)](https://platform.openai.com/docs/guides/evals?api-mode=responses)
  - [ ] Analytics research (AI-powered or Statista powered): wedding costs
  - [ ] Explore with different combinations of input parameters
  - [ ] Assess if the results are consistent - Quick notebook with a couple of viz should help here. 
  - [ ] Assess if the allocated budget per category makes sense.
- [ ] (If needed) Analytics script / notebook:
  - [ ] Budget total
  - [ ] Categories (present or missing) / allocated budget 
  - [ ] Variations across iterations (box plots, missing categories, total percentage of each category with respect to the total budget)
- [ ] Prompt 03: Web research within the prompt (different model? or endpoint?)
  - [ ] [Deep Research within OpenAI API](https://cookbook.openai.com/examples/deep_research_api/introduction_to_deep_research_api?utm_source=chatgpt.com)
  - [ ] Check resources here for deep research within the API - https://openai.com/startups/?utm_source=linkedin
- [ ] Prompt 04: Hierarchichal prompt 
- [ ] Explore different models, feats (context window, problem-solving capability, etc.)
  - [ ] Use OpenAI python library
- [ ] Test models
    - [ ] Variations: prompt01 (no research) 
    - [ ] OpenAI (different models)
    - [ ] Gemini
    - [ ] Perplexity
    - [ ] Claude
- [ ] Possible enhancements:
  - [ ] Deep research or web search within the prompt
        ```
        ## Research Requirements
        - Find actual minimum costs for each service in the specified location
        - Research typical per-guest catering costs for the area
        - Understand what venues typically include (catering, decoration, etc.)
        - Consider package deals common in the location
        ```
  - [ ] Make the prompt modular (function calling)
  - [ ] Pull from an existing data base
  - [ ] Add a contingency category
  - [ ] Define behaviour when no reasonable budget allocation is found
  - [ ] Iterate the budget if the constraints are not fulfilled or the budget is not used up. 
  - [ ] Meta-prompting on each model --> Probably the best way to have each model define the best way to talk to itself.


## Use Case

### Use Case Scoping
Create an initial budget allocation for a wedding given a set of input parameters and some contraints defined on the system side. 
The output should be provided as a JSON string with key/value (k/v) parameters that represent the categories (k) and assigned budget (v). 

Note: the budget allocation could be:
- An educated guess that is *sensible* given the available budget, geographical location and number of guests. 
- A proposal based on researched values of how much it costs to organise a wedding in the specified cities, with the given number of guests

For example: A wedding in Madrid (Spain) with 50k budget and 150 guests could have the following budget allocation:
```
{
    "venue": 5000,
    "florist": "500",
    "total_guest_budget": 15000, # 100 * 150 = 15,000
    "bride_attire": "2000",
    "groom_attire": "1000",
}
```

### Open questions:
* Do we want to include all subcategories in the beginning?
  * ==> * Do we allow for "wedding" types: budget, luxury, "sensible", ...
  * Depending on the wedding type, we include or leave out certain categories
* Do we want to have contingency category for emergencies or unexpected costs?
* Do we iterate the budget?
* Data bases with budget allocations based on different segmentation categories: geographical, age, culture, etc.
* Do we need prompts / country / culture, etc.?
* How do we validate budget?
* Should culture be included as a parameter to design the budget allocation?
* How to develop a modular prompt to implement a hierarchical prompt?


## Prompt Scoping

Inputs:
* Wedding location
* Number of guests
* Max budget

Categories:
* Percentage for venue + catering (assumption that the catering comes with the venue)
* Guests budget:
  * Gifts
* Percentage for florist
* Percentage for bride/groom attire(s)
* Percentage for music/entertainment
* Percentage for officiant
* Percentage for makeup artist and hairdressing
* Percentage for photographer
* Percentage for stationary (save the dates, invites, ...)
* Percentage for contingency

Considerations:
* Initial budget allocation
* 

Output format:
* Json string with k/v pairs
* Each k/v pair is a category

## Prompt 01: Propose an educated guess based on pre-defined values
* Role
* Context:
  * Overarching task
  * Input values
* Task (Step-wise):
  * Depending on the overall budget, assign a type to the wedding. 
    * Three categories: low, medium, high
    * Examples...
  * Collect the list of categories that the budget will be distributed among depending on the wedding type
  * (If any) Collect contraints for budget calculation
    * The total sum of each category's assigned budget should not exceed the available budget
    * In this step, is where we could apply deep research
  * Calculate the budget amount for each category considering the constraints
  * Create a json file with the calculated budget
  * (Optional) Iterate budget

### Observations

    Budget Variations:
      - File 1 (2025-08-30): Total ~$49,000, 16 categories
      - File 2 (2025-08-31 21:27): Total ~$49,550, 15 categories (missing guest transportation)
      - File 3 (2025-08-31 21:34): Total ~$49,100, 15 categories (missing photo booth)

    Key Differences:
      - Catering costs vary significantly: $18,000 → $17,500 → $20,000
      - Some categories missing in later runs (transportation, photo booth)
      - Token usage fluctuates: 5,475 → 4,820 → 5,907
      - Debug mode was enabled for the last two runs

    Observations:
      - Consistent prompt file usage (./prompts/prompt_01.txt)
      - Model consistently using gpt-5
      - Similar budget totals despite category variations
      - Standard wedding expense categories represented

## Prompt 03: Propose an budget based on research done upon request of the budget

## General Notes
- App users will have the option to add custom categories in addition to the default ones in the app. 


## Resources

### [Insta post with coarse prompting guidelines for GPT-5](https://www.instagram.com/p/DNWWiSZyYfT/?igsh=MXRkbWlqZmYweXZhNw%3D%3D)
      - Role
      - Task
      - Context, limitations and examples
      - Reasoning: Reflect on the problem and share the logic reasoning before answering
      - Provide desired output format
      - Specify end conditions 
  
### [OpenAI Resource Hub](https://openai.com/startups/)


## Backup

### [Gemini] Initial research of tentative budget allocations across predefined categories
***Prompt***
<div style="border: 1px solid #333; padding: 10px; background-color: white; color: black;">
You are an experienced and successful wedding planner.
I need to organise a wedding. Your task is to help me with the management of this project.
I need to start with my budget allocation. Propose a reasonable budget allocation across the following categories:

  * Percentage for venue: 10%
  * Percentage for florist
  * Budget for guests:
    * Catering (meal, drinks)
    * Gifts
  * Percentage for bride/groom attire(s)
  * Percentage for music/entertainment
  * Percentage for officiant
  * Percentage for makeup 
</div>

***Response***
<div style="border: 1px solid #333; padding: 10px; background-color: white; color: black;">

## Overall Budget Allocation (as a percentage of your total budget):

**Venue (including catering and drinks): 40-50%**
• This is typically the largest single expense
• Often includes the cost of the space itself, the food, and the beverage package
• This is where the majority of your budget will go, as it dictates the number of guests you can have and the overall ambiance of your wedding

**Florist: 8-10%**
• Covers bouquets, boutonnieres, ceremony arrangements, and reception centerpieces
• The final cost can vary significantly based on the types of flowers you choose and the complexity of the arrangements

**Bride/Groom Attire(s): 5-8%**
• Includes the wedding gown, tuxedo or suit, shoes, and any accessories
• Remember to also factor in alteration costs, which can add up

**Music/Entertainment: 7-10%**
• Can include a DJ, a live band, or a combination of both for the ceremony, cocktail hour, and reception
• A good music selection sets the tone for the entire event, so it's a worthwhile investment

**Officiant: 1-2%**
• Covers the fee for a professional officiant to perform your ceremony
• Can vary widely depending on whether you choose a religious figure, a civil celebrant, or a friend who becomes ordained for the day

**Makeup and Hair: 1-2%**
• Includes the cost for professional hair and makeup artists for the bride and potentially the bridal party
• Trial runs are often included in the cost or charged separately

## Per-Person Budget Breakdown:

Beyond the percentages, it's crucial to have an idea of your minimum per-person costs, which primarily relate to your guests.

**Catering (Meal & Drinks):**
• Can range from €50 to €250+ per person, depending on:
  - Menu selection
  - Service style (e.g., buffet vs. plated dinner)
  - Beverage package
• This figure is often bundled with the venue cost, so check what is included in your venue's quote
• A basic catering package in a more rural area might be at the lower end of this range, while a high-end, urban venue with premium menu options will be at the higher end

**Gifts:**
• €10-30 per person for wedding favors or small gifts for guests
• This is often one of the first areas couples consider cutting if the budget is tight
• Consider personalized items that guests will actually use and appreciate

## Additional Categories to Consider:
While not on your initial list, these are essential for a complete budget and successful planning:

* Photography/Videography: 10-12%
* Stationery (Invitations, Save-the-Dates): 2-3%
* Wedding Planner: 10-15% (for full-service planning)
* Wedding Rings: 2-3%
* Miscellaneous/Contingency Fund: 5-10% (Crucial for unexpected costs!)
* Other (rentals, transportation, hotel room for the night of, etc.): 5%

</div>


### OpenAI API

- Role: "System" is used to set the tone fo the chat
- Role: "User" is used to indicate that the message comes from the user. 
- Role: "assisstant" text created by the chatbot
- We could use the n parameters to request multiple budgets at once
- Temperature controls randomness into the output. It does not seem useful for this case, but it would be good to keep it in mind. 

### Note on used tokens
There are several reasons why completion tokens can be higher than prompt tokens even when the visible text is shorter:

  1. Token encoding efficiency varies: Some words/phrases tokenize into fewer tokens than others. The AI's JSON response might use words that require more tokens per character.
  1. Hidden processing tokens: The completion count may include internal processing tokens that aren't visible in the final output - reasoning, formatting decisions, etc.
  1. Your prompt file: Your actual prompt is in ./prompts/prompt_01.txt (1,686 tokens). This might be more concise than you think, or use efficiently-tokenized language.
  1. JSON structure overhead: The structured JSON format with long category names like "WEDDING_SUBCATEGORY_WEDDING_VENUES" is token-expensive.
  1. Model-specific tokenization: Different models tokenize text differently. Some phrases might tokenize more efficiently than others.