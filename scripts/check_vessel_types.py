#!/usr/bin/python
import re
import yaml

vessel_groups = set()
vessel_types = {}
vessel_code = {}

with open('vessel_types.csv', 'r') as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue
            
            fields = line.strip().split(",")

            if len(fields) < 2:
                continue

            vessel_group = fields[0]
            vessel_groups.add(vessel_group)

            vessel_type = fields[1]
            from_to = vessel_type.split("-")
            classification = ' '.join(fields[3:])

            #ais_vessel_code = fields[2]
            data = {
                     'vessel_group': vessel_group,
                     'classification': classification
                   }

            if len(from_to) == 1:
                vessel_types[int(from_to[0])] = data
            elif len(from_to) == 2:
                for i in range(int(from_to[0]), int(from_to[1])+1):
                    vessel_types[i] = data

with open('vessel_types.yaml', 'w') as f:
    yaml.dump(vessel_types, f)
