def get_claim():

    disease = input("Disease: ").strip()

    days = int(
        input("Hospitalization Days: ")
    )

    return {
        "disease": disease,
        "days": days
    }