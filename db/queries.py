def get_fabrication_centers_query():
    return "SELECT * FROM centro_de_fabricacion"

def get_distribution_centers_query():
    return "SELECT * FROM centro_de_distribucion"

def get_points_of_sale_query():
    return "SELECT * FROM punto_de_venta"

def get_scenarios_query():
    return "SELECT * FROM escenario"

def insert_fabrication_center_query():
    return "INSERT INTO centro_de_fabricacion (nombre, data) VALUES (%s, %s);"

def insert_distribution_center_query():
    return "INSERT INTO centro_de_distribucion (nombre, data) VALUES (%s, %s);"

def insert_point_of_sale_query():
    return "INSERT INTO punto_de_venta (nombre, data) VALUES (%s, %s);"

def insert_scenario_query():
    return "INSERT INTO escenario (nombre, data) VALUES (%s, %s);"