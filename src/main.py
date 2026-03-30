import logging
import traceback
from src.Sources.file_source import File_Source
from random import randint
from src.Sources.api_source import Api_source
from src.Sources.generator_source import Generator_source
from src.Constans.constans_type import TYPE_SOURCE
from src.Patterns.pattern_source import Sources


def main() -> None:
    """
    Основная функция взаимодействия с пользователем
    """
    source_dict = {}
    while True:
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        command = input("Select command (create_source, get_task, get_all_tasks, exit): ")
        logging.info(f"Select command (create_source, get_task, get_all_tasks): {command}")
        if command == "exit":
            exit()
        if command not in ["create_source", "get_task", "get_all_tasks"]:
            print("Error: no such command")
            logging.error("Error: no such command")
        else:
            source_name = input("Enter source name: ")
            logging.info(f"Enter source name: {source_name}")
            if source_name not in list(source_dict.keys()) and command == "create_source":
                source_type = input("Select a source (file, generator, api): ")
                logging.info(f"Select a source (file, generator, api): {source_type}")
                if source_type not in ["file", "generator", "api"]:
                    print("Error: no such source type")
                    logging.error("Error: no such source type")
                else:
                    if isinstance(TYPE_SOURCE[source_type], Sources):
                        source = TYPE_SOURCE[source_type].create_source(source_name)
                        source_dict[source_name] = source
                    else:
                        print("Error: non-compliance with protocol")
                        logging.error("Error: non-compliance with protocol")
            elif source_name in list(source_dict.keys()) and command != "create_source":
                if isinstance(source_dict[source_name], Sources):
                    if command == "get_task":
                        try:
                            text_task = source_dict[source_name].get_task()
                            print(text_task)
                            logging.info(text_task)
                        except ValueError as e:
                            print(e)
                            logging.error(e)
                    elif command == "get_all_tasks":
                        try:
                            text_tasks = source_dict[source_name].get_all_tasks()
                            for task in text_tasks:
                                print(task)
                                print("\n")
                                logging.info(task)
                        except:
                            print(e)
                            logging.error(e)
                else:
                    print("Error: non-compliance with protocol")
                    logging.error("Error: non-compliance with protocol")
            elif source_name in list(source_dict.keys()) and command == "create_source":
                print("Error: source with such name already exsist. Change name of source")
                logging.error("Error: source with such name already exsist. Change name of source")
            else:
                print("Error: no such source. Please, create it")
                logging.error("Error: no such source. Please, create it")

if __name__ == "__main__":
    main()
