from bs4 import BeautifulSoup
import json


def read_and_parse_file(file_name):
    # opening file
    with open(file_name, 'r') as f:
        data = f.read()
    # Passing the stored data inside the beautifulsoup parser
    bs_data = BeautifulSoup(data, 'xml')
    # Finding all instances of entry tag
    return bs_data.find_all('entry')


def parse_por():
    entries = read_and_parse_file('ProductOrderRouting.xml')

    arr = []
    for entry in entries:
        obj = {"status": entry.find("Status").text, "prod_order_no": entry.find("Prod_Order_No").text,
               "routing_reference_no": entry.find("Routing_Reference_No").text,
               "routing_no": entry.find("Routing_No").text,
               "operation_no": entry.find("Operation_No").text,
               "next_operation_no": entry.find("Next_Operation_No").text,
               "previous_operation_no": entry.find("Previous_Operation_No").text, "type": entry.find("Type").text,
               "no": entry.find("No").text, "work_center_no": entry.find("Work_Center_No").text,
               "description": entry.find("Description").text, "setup_time": entry.find("Setup_Time").text,
               "run_time": entry.find("Run_Time").text, "routing_link_code": entry.find("Routing_Link_Code").text,
               "starting_time": entry.find("Starting_Time").text, "starting_date": entry.find("Starting_Date").text,
               "ending_time": entry.find("Ending_Time").text, "ending_date": entry.find("Ending_Date").text,
               "output_quantity": entry.find("Output_Quantity").text,
               "scrap_quantity": entry.find("Scrap_Quantity").text}
        arr.append(obj)

    return arr


def parse_cle(por_entries):
    entries = read_and_parse_file('CapacityLedgerEntry.xml')

    arr = []
    for entry in entries:
        obj = {"entry_no": entry.find("Entry_No").text, "order_no": entry.find("Order_No").text,
               "order_line_no": entry.find("Order_Line_No").text, "routing_no": entry.find("Routing_No").text,
               "routing_reference_no": entry.find("Routing_Reference_No").text,
               "operation_no": entry.find("Operation_No").text, "item_no": entry.find("Item_No").text,
               "variant_code": entry.find("Variant_Code").text, "posting_date": entry.find("Posting_Date").text,
               "type": entry.find("Type").text, "no": entry.find("No").text,
               "work_center_no": entry.find("Work_Center_No").text, "description": entry.find("Description").text,
               "quantity": entry.find("Quantity").text, "setup_time": entry.find("Setup_Time").text,
               "run_time": entry.find("Run_Time").text, "stop_time": entry.find("Stop_Time").text,
               "cap_unit_of_measure_code": entry.find("Cap_Unit_of_Measure_Code").text,
               "qty_per_cap_unit_of_measure": entry.find("Qty_per_Cap_Unit_of_Measure").text,
               "output_quantity": entry.find("Output_Quantity").text,
               "scrap_quantity": entry.find("Scrap_Quantity").text,
               "unit_of_measure_code": entry.find("Unit_of_Measure_Code").text,
               "qty_per_unit_of_measure": entry.find("Qty_per_Unit_of_Measure").text, "operations": []}

        por_entries_copy = []
        for por_entry in por_entries:
            if por_entry["routing_no"] == obj["routing_no"]:
                obj['operations'].append(por_entry)
            else:
                por_entries_copy.append(por_entry)
        por_entries = por_entries_copy
        arr.append(obj)
    return arr


def format_cle(data_mo, order_no_dict):
    for entry in data_mo:
        entry['poh'] = order_no_dict[entry["order_no"]]


def parse_pol():
    entries = read_and_parse_file('ProductOrderLine.xml')

    dt = {}
    for entry in entries:
        obj = {"status": entry.find("Status").text, "prod_order_no": entry.find("Prod_Order_No").text,
               "line_no": entry.find("Line_No").text, "item_no": entry.find("Item_No").text,
               "variant_code": entry.find("Variant_Code").text, "description": entry.find("Description").text,
               "description_2": entry.find("Description_2").text, "quantity": entry.find("Quantity").text,
               "finished_quantity": entry.find("Finished_Quantity").text,
               "remaining_quantity": entry.find("Remaining_Quantity").text,
               "unit_of_measure_code": entry.find("Unit_of_Measure_Code").text,
               "starting_date": entry.find("Starting_Date").text, "starting_time": entry.find("Starting_Time").text,
               "ending_date": entry.find("Ending_Date").text, "ending_time": entry.find("Ending_Time").text,
               "routing_no": entry.find("Routing_No").text,
               "routing_reference_no": entry.find("Routing_Reference_No").text, "eTag": entry.find("ETag").text}
        dt[obj["prod_order_no"]] = obj
    return dt


def parse_poc(source_dict):
    entries = read_and_parse_file('ProductOrderComponent.xml')

    arr = []
    for entry in entries:
        obj = {}
        obj["status"] = entry.find("Status").text
        obj["prod_order_no"] = entry.find("Prod_Order_No").text
        obj["prod_order_Line_no"] = entry.find("Prod_Order_Line_No").text
        obj["line_no"] = entry.find("Line_No").text
        obj["item_no"] = entry.find("Item_No").text
        obj["variant_code"] = entry.find("Variant_Code").text
        obj["description"] = entry.find("Description").text
        obj["description_2"] = entry.find("Description_2").text
        obj["quantity_per"] = entry.find("Quantity_per").text
        obj["expected_quantity"] = entry.find("Expected_Quantity").text
        obj["remaining_quantity"] = entry.find("Remaining_Quantity").text
        obj["act_Consumption_qty"] = entry.find("Act_Consumption_Qty").text
        obj["unit_of_Measure_code"] = entry.find("Unit_of_Measure_Code").text
        obj["routing_Link_code"] = entry.find("Routing_Link_Code").text
        obj["eTag"] = entry.find("ETag").text
        obj["poh"] = source_dict.get(obj["item_no"])
        arr.append(obj)
    return arr


def format_poh(data_poc, data_p):
    poc_entries = data_poc[:]

    for entry in data_p:
        entry['poc'] = []
        poc_entries_copy = []
        for poc_entry in poc_entries:
            if poc_entry["prod_order_no"] == entry["no"]:
                entry['poc'].append(poc_entry)
            else:
                poc_entries_copy.append(poc_entry)
        poc_entries = poc_entries_copy[:]

    return


def parse_poh(data_pol):
    entries = read_and_parse_file('ProductOrderHeader.xml')

    data_p = []
    source_dict = {}
    order_no_dict = {}
    for entry in entries:
        obj = {"status": entry.find("Status").text, "no": entry.find("No").text,
               "description": entry.find("Description").text, "description_2": entry.find("Description_2").text,
               "search_description": entry.find("Search_Description").text,
               "source_type": entry.find("Source_Type").text, "source_no": entry.find("Source_No").text,
               "starting_time": entry.find("Starting_Time").text, "starting_date": entry.find("Starting_Date").text,
               "ending_time": entry.find("Ending_Time").text, "ending_date": entry.find("Ending_Date").text,
               "due_date": entry.find("Due_Date").text, "sales_order_no": entry.find("Sales_Order_No").text,
               "eTag": entry.find("ETag").text}
        obj["pol"] = data_pol[obj["no"]]
        source_dict[obj["source_no"]] = obj
        order_no_dict[obj["no"]] = obj
        data_p.append(obj)
    return {"data_p": data_p, "source_dict": source_dict, "order_no_dict": order_no_dict}


# here in main we are going to create two main list of objects
# 1- Creating manufacturing order using cle and por file
# 2- Creating product using poc, pol and poh files

def main():

    # formatting and parsing cle data
    data_por = parse_por()
    # cle is basically manufacturing order (mo)
    data_mo = parse_cle(data_por)

    # parsing pol data
    data_pol = parse_pol()

    # parsing poh data and assigning pol to POH object
    poh_data = parse_poh(data_pol)
    data_p = poh_data["data_p"]

    # source dictionary contains the poh data against source number key
    source_dict = poh_data["source_dict"]

    # order no dictionary contains the poh data against order number key
    order_no_dict = poh_data["order_no_dict"]

    # parsing poc and assigning poh child if poc item number is same source number of poh
    data_poc = parse_poc(source_dict)

    # formatting the poh data again and this time assigning poc list
    format_poh(data_poc, data_p)

    # formatting the mo data again and this time assigning poh object
    format_cle(data_mo, order_no_dict)

    # storing dictionaries to txt files
    with open('mo.txt', 'w') as f:
        f.write(json.dumps(data_mo))

    with open('products.txt', 'w') as f:
        f.write(json.dumps(data_p))

    with open('poc.txt', 'w') as f:
        f.write(json.dumps(data_poc))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

