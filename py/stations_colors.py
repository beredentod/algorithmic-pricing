'''
File: stations_colors.py

- color of each brand for visualization
'''

def hex_to_rgb(hex_code):
    # Remove the '#' symbol if it's present
    if hex_code[0] == '#':
        hex_code = hex_code[1:]
    
    # Convert the hex code to (r, g, b) values
    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0
    
    # Return the normalized (r, g, b) tuple
    return (r, g, b)


colors_brands = {
'aral': '#2596be', #blue
'shell': '#ffcd00', #yellow
'agip': '#000000', #black
'esso': '#da0013', #red
'jet': '#ffce39', #yellow
'omv': '#00457c', #blue
'allguth': '#ed194c', #reddis
'sonstige': '#d3d3d3', #light grey
'other': '#d3d3d3', #light grey
'total': '#fc0103', #red
'avia': '#ed194c', #red
'bavaria petrol': '#3773b3', #blue
'sprint': '#be1a31', #darker red
'v-markt': '#f18700', #orange
'hem': '#82b226', #green
'bk': '#1e3e8b', #blue
'sued treibstoff': '#970d22', #reddish
'oil!': '#691e79', #violet
'mr wash': '#f04220', #red-orange
'star': '#ed1c24', #red
'bft': '#ee7100', #orange
'raiffeisen': '#62af15', #green
'other_integrated': '#964b00', #brown
'non-integrated': '#d3d3d3', #light grey
'aggregate': '#8f00ff' #violet
}
