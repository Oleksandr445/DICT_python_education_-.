def show_help():
    print(
        "Available formatters: plain bold italic header link inline-code "
        "ordered-list unordered-list new-line"
    )
    print("Special commands: !help !done")


def get_int_input(prompt, error_message, min_value=None, max_value=None):
    while True:
        value = input(prompt)

        if not value.isdigit():
            print(error_message)
            continue

        value = int(value)

        if min_value is not None and value < min_value:
            print(error_message)
            continue

        if max_value is not None and value > max_value:
            print(error_message)
            continue

        return value


def main():
    markdown = ""

    while True:
        command = input("Choose a formatter: > ")

        if command == "!help":
            show_help()
            continue

        if command == "!done":
            with open("output.md", "w", encoding="utf-8") as file:
                file.write(markdown)
            break

        if command == "plain":
            text = input("Text: > ")
            markdown += text

        elif command == "bold":
            text = input("Text: > ")
            markdown += f"**{text}**"

        elif command == "italic":
            text = input("Text: > ")
            markdown += f"*{text}*"

        elif command == "inline-code":
            text = input("Text: > ")
            markdown += f"`{text}`"



        elif command == "new-line":
            markdown += "\n\n"

        elif command == "header":
            level = get_int_input(
                "Level: > ",
                "The level should be within the range of 1 to 6",
                min_value=1,
                max_value=6
            )
            text = input("Text: > ")
            markdown += "#" * level + " " + text + "\n\n"

        elif command == "link":
            label = input("Label: > ")
            url = input("URL: > ")
            markdown += f"[{label}]({url})"


        elif command in ("ordered-list", "unordered-list"):
            rows = get_int_input(
                "Number of rows: > ",
                "The number of rows should be greater than zero",
                min_value=1
            )

            if markdown and not markdown.endswith("\n"):
                markdown += "\n"

            for i in range(1, rows + 1):
                row = input(f"Row #{i}: > ")
                if command == "ordered-list":
                    markdown += f"{i}. {row}\n"
                else:
                    markdown += f"* {row}\n"


            markdown += "\n"

        else:
            print("Unknown formatting type or command")
            continue

        print(markdown)


if __name__ == "__main__":
    main()
