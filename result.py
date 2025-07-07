def result(question,model):
    response = model.generate_content(
    question)
    print(response.candidates)
    return response.text
