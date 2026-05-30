import asyncio
import logging
from random import randint
from src.Constans.constans_type import TYPE_SOURCE
from src.Patterns.pattern_source import Sources

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
async def main() -> None:
    """
    Основная функция взаимодействия с пользователем
    """
    source_dict = {}
    while True:
        command = await asyncio.to_thread(input, "Select command (create_source, get_task, get_all_tasks, exit): ")
        logging.info(f"Select command (create_source, get_task, get_all_tasks): {command}")
        if command == "exit":
            exit()
        if command not in ["create_source", "get_task", "get_all_tasks"]:
            print("Error: no such command")
            logging.error("Error: no such command")
        else:
            source_name = await asyncio.to_thread(input, "Enter source name: ")
            logging.info(f"Enter source name: {source_name}")
            if source_name not in list(source_dict.keys()) and command == "create_source":
                source_type = await asyncio.to_thread(input, "Select a source (file, generator, api): ")
                logging.info(f"Select a source (file, generator, api): {source_type}")
                if source_type not in ["file", "generator", "api"]:
                    print("Error: no such source type")
                    logging.error("Error: no such source type")
                else:
                    if isinstance(TYPE_SOURCE[source_type], Sources):
                        source = await TYPE_SOURCE[source_type].create_source(source_name)
                        source_dict[source_name] = source
                    else:
                        print("Error: non-compliance with protocol")
                        logging.error("Error: non-compliance with protocol")
            elif source_name in list(source_dict.keys()) and command != "create_source":
                if isinstance(source_dict[source_name], Sources):
                    if command == "get_task":
                        try:
                            text_task = await source_dict[source_name].get_task()
                            print(text_task)
                            logging.info(text_task)
                        except ValueError as e:
                            print(e)
                            logging.error(e)
                    elif command == "get_all_tasks":
                        filter = await asyncio.to_thread(input, "Select filter (None, Status, Priority): ")
                        if filter not in ["None", "Status", "Priority"]:
                            print("Error: no such filter")
                            logging.error("Error: no such filter")
                        elif filter  == "Status":
                            filter = await asyncio.to_thread(input, "Select status (Over, In work): ")
                            if filter not in ["Over", "In work"]:
                                print("Error: no such status")
                                logging.error("Error: no such status")
                        elif filter == "Priority":
                            filter = await asyncio.to_thread(input, "Select priopity (High, Normal, Very high): ")
                            if filter not in ["High", "Normal", "Very high"]:
                                print("Error: no such priority")
                                logging.error("Error: no such priority")
                        try:
                            tasks = await source_dict[source_name].get_all_tasks(filter)
                            for task in tasks:
                                print(task)
                                print("\n")
                        except ValueError as e:
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
     asyncio.run(main())
