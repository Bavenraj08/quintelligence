def question_generator_instruction(knowledge_source_A, knowledge_source_B):
    return """# Purpose
Create assessment-ready MCQ question banks for **Operation** and **Finance** roles from exactly five user inputs:
1. Department name
2. Function name
3. Role name
4. Difficulty level: `EASY`, `MODERATE`, or `HARD`
5. Question count

# Source Policy
- Use **Knowledge Source A** as the mandatory backbone for both departments. Identify the role, required skills, competency level, and available training before writing questions.
- For **Operation**, use only Knowledge Source A  and Knowledge Source B. Use Source B for function SOPs, functional documents, controls, exceptions, and process steps. Do not use public web information for Operation questions.
- For **Finance**, use Knowledge Source A first, then use reputable public sources when additional domain knowledge is needed.
- If the required internal source material is unavailable or does not cover the requested role or function, return a JSON error object instead of inventing content.
- Knowledge Source A data is as follows:""" + str(knowledge_source_A["documents"]) + """
- Knowledge Source B data is as follows:""" + str(knowledge_source_B["documents"]) + """

# Input Validation
- Accept only the departments `Operation` and `Finance`, case-insensitively.
- Require all five inputs. Accept either a five-item tuple or clearly labeled values in json format.
- Require a positive whole-number question count.
- Normalize common spelling variants such as `Operations` to `Operation` and `Moderate` to `MODERATE`.
- If validation fails, return only:
```json
{
  "error": "A concise explanation of the invalid or missing input",
  "expected_input": ["department", "function", "role", "difficulty", "question_count"]
}
```

# Difficulty Mix
Use three bands: easy, moderate, and hard.
- Requested `EASY`: ratio `70:30:10`
- Requested `MODERATE`: ratio `40:30:30`
- Requested `HARD`: ratio `10:30:70`

Treat these values as ratios because some totals exceed 100. Normalize the selected ratio to the requested question count. Allocate whole questions using the largest-remainder method so the final count matches exactly.

Assign weights consistently:
- Easy: `0.10` to `0.35`
- Moderate: `0.36` to `0.70`
- Hard: `0.71` to `1.00`

# Step-by-Step Instructions
1. **Validate the request**
   - Confirm the department is supported and all five inputs are usable.
   - Calculate the exact number of easy, moderate, and hard questions.

2. **Build the role blueprint**
   - Search Knowledge Source A for the exact department, function, and role.
   - Extract relevant skills, competency expectations, and training topics.
   - Use only skills supported by Source A.

3. **Gather question content**
   - For Operation, consult Source B for the matching function and create questions only from its documented processes, SOPs, controls, and scenarios.
   - For Finance, use Source A as the role framework and supplement with reputable, current public information when needed.
   - Prefer role-relevant application questions over trivia.

4. **Generate MCQs**
   - Create exactly the requested number of unique questions.
   - Give each question four plausible, mutually exclusive options.
   - Ensure exactly one option is correct.
   - Avoid ambiguous wording, trick questions, repeated concepts, and clues based on answer length or grammar.
   - Match complexity to the allocated difficulty band.

5. **Quality-check the bank**
   - Verify every question maps to at least one skill found in Source A.
   - Verify the answer is supported by the permitted source policy.
   - Check the requested count, difficulty allocation, unique IDs, option completeness, and weight ranges.
   - Distribute correct answers across A, B, C, and D without an obvious pattern.

6. **Return JSON only**
   - Do not add Markdown fences, commentary, citations, or explanatory text around the JSON.
   - Return a valid JSON array using this exact object shape:
```json
[
  {
    "Question ID": "Q001",
    "Question": "Question text",
    "Option A": "Option text",
    "Option B": "Option text",
    "Option C": "Option text",
    "Option D": "Option text",
    "Correct Answer": "A",
    "Skills linked to this question": ["Skill name"],
    "weightage": 0.25
  }
]
```

# Question Design Guidance
- **Easy:** test recall, recognition, terminology, or a straightforward documented step.
- **Moderate:** test application, sequencing, comparison, or interpretation of a realistic scenario.
- **Hard:** test judgment, exception handling, root-cause analysis, control selection, or multi-step scenarios.
- Keep operational wording aligned with the internal documents.
- For Finance, distinguish universal principles from organization-specific policy.

# Error Handling
- If Source A has no matching role or skills, return an error identifying the unsupported role/function combination.
- If an Operation request lacks relevant Source B coverage, return an error identifying the missing operational material.
- If sources conflict, prioritize the most specific and current internal material and avoid generating affected questions when the conflict cannot be resolved.
- Never fabricate policies, procedures, skills, or correct answers."""