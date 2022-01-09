from os import stat
import os
import xml.etree.ElementTree as ET
from boardgame import boardgame as BG

class data_parser:

    def get_default_name(self, name_elements_list: ET.Element):
        for name_element in name_elements_list:
            if name_element.get("type") == "primary":
                return name_element.get("value")

    def get_statistics(self, element_statistics: ET.Element, output_type: str):
        stats = []
        if output_type == "text":
            wanted_stats = ["average", "owned", "wanting", "trading", "wishing"]
            for stat in wanted_stats:
                stats.append(f"\t{stat.capitalize()}: " + self.get_specific_data_from_item(element_statistics, stat))
            return "\n".join(stats)
        else:
            wanted_stats = ["average", "owned", "wanting", "trading", "wishing"]
            for stat in wanted_stats:
                stats.append(self.get_specific_data_from_item(element_statistics, stat))
            return stats

    def get_specific_data_from_item(self, item: ET.Element, data):
        return item.find(data).get("value")

    def get_element_extra_data(self, item_extra_data: ET.Element, extra_data_type, output_type: str):
        datas = []
        for extra_data in item_extra_data:
            if extra_data.get("type") == extra_data_type:
                datas.append(extra_data.get("value"))
        if output_type == 'text':
            return ", ".join(datas)
        else:
            return datas

    def get_quantity_of_players(self, item: ET.Element, output_type: str):
        item_min_players = self.get_specific_data_from_item(item, "minplayers")
        item_max_players = self.get_specific_data_from_item(item, "maxplayers")
        if output_type == 'text':
            return f"min_players {item_min_players}, max_players {item_max_players}"
        else:
            return (item_min_players, item_max_players)

    # Global variables
    output_type = 'csv'
    file_name = 'data'
    
    def __init__(self, file_name, output_type, input_file) -> None:
        self.output_type = output_type
        self.file_name = file_name
        self.input_file = input_file

    def main(self, delete_old_data: bool = True):
        if self.output_type != 'text':
            if delete_old_data == True:
                try:
                    os.remove(self.file_name + '.' + self.output_type)
                except:
                    1
        try:
            tree = ET.parse(self.input_file + ".xml")
            root = tree.getroot()

            if root: print("XML loaded succesfully")

            items = tree.findall("item")
            extra_data_types = ["boardgamecategory", "boardgamemechanic", "boardgamepublisher", "boardgamedesigner", "boardgameartist"]

            print(f"Loaded {len(items)} items")
            if self.output_type == 'text':
                # Visual part
                print("\nItems:")
                for item in items:
                    item_id = item.get("id")
                    print(f"\nItem's id: {item_id}")
                    print(f"\tName: " + self.get_default_name(list(item.iter("name"))))
                    print("\t" + self.get_quantity_of_players(item, self.output_type))
                    print( "\tpublished " + self.get_specific_data_from_item(item, "yearpublished"))
                    print("\t" + item.find("description").text)
                    item_extra_data = list(item.iter("link"))
                    for extra_type in extra_data_types:
                        print("\t" + extra_type.replace("boardgame", "").capitalize() + ":")
                        print("\t\t" + self.get_element_extra_data(item_extra_data, extra_type, self.output_type))
                    item_statistics = item.find("statistics").find("ratings")
                    print(self.get_statistics(item_statistics, self.output_type))
            else:
                games_list: list[BG] = []
                # Data part
                for item in items:
                    item_id: int = item.get("id")
                    item_title: str = self.get_default_name(list(item.iter("name")))
                    bg = BG(item_id, item_title)
                    
                    item_min_players, item_max_players = self.get_quantity_of_players(item, self.output_type)
                    bg.set_max_players(item_max_players).set_min_players(item_min_players)
                    
                    item_year_published = self.get_specific_data_from_item(item, "yearpublished")
                    bg.set_year_of_publishing(item_year_published)
                    
                    item_description = item.find("description").text
                    bg.set_description(item_description)
                    
                    item_extra_data = list(item.iter("link"))
                    bg.set_category(self.get_element_extra_data(item_extra_data, "boardgamecategory",self.output_type)).set_mechanics(self.get_element_extra_data(item_extra_data, "boardgamemechanic",self.output_type))
                    bg.set_publishers(self.get_element_extra_data(item_extra_data, "boardgamepublisher",self.output_type)).set_designer(self.get_element_extra_data(item_extra_data, "boardgamedesigner",self.output_type)).set_artists(self.get_element_extra_data(item_extra_data, "boardgameartist",self.output_type))
                    
                    item_statistics = item.find("statistics").find("ratings")
                    stats = self.get_statistics(item_statistics, self.output_type)
                    bg.set_rating(stats[0]).set_owned(stats[1]).set_wanting(stats[2]).set_trading(stats[3]).set_wishing(stats[4])
                    
                    games_list.append(bg)
                
                if self.output_type == 'json':
                    with open(f'./{self.file_name}.json', 'a') as f:
                        if delete_old_data == True:
                            f.write('[')
                        for elem in games_list:
                            f.write(elem.__dict__.__str__().replace("'", "\""))
                            f.write(',')
                        if delete_old_data == False:
                            f.write('{}]')
                if self.output_type == 'csv':
                    with open(f'./{self.file_name}.csv', 'a') as f:
                        if delete_old_data == True:
                            columns = ['id', 'title', 'description', 'rating', 'min_players', 'max_players',
                                'year_of_publishing', 'artists', 'category', 'designer', 'mechanics',
                                'publishers', 'owned', 'wanting', 'trading', 'wishing']
                            f.write(', '.join(columns) + '\n')
                        for elem in games_list:
                            f.write(elem.csvize() + '\n')
            
            return len(items)
        except:
            return 0    
        