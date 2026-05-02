from pipeline import process_single_file


def classify_file(path):
    result = process_single_file(path)
    result_upper = result.upper()

    if "SELFIE" in result_upper:
        return result, "selfies"

    elif "NON-SELFIE" in result_upper:
        return result, "others"

    elif "RESUME" in result_upper:
        return result, "resumes"

    elif "OTHER DOCUMENT" in result_upper:
        return result, "documents"

    else:
        return result, "others"