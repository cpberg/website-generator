import craiyon

def generate_image_with_craiyon(prompt):
    generator = craiyon.Craiyon()
    result = generator.generate(prompt)
    return result.images

