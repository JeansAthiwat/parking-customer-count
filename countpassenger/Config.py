import os
import os.path as osp

class Config():
    
    def __init__(self, *args, **kwargs):
        
        self.BASE_DIR = '/home/jeans/internship/parking-customer-count'
        self.RESOURCES_DIR = osp.join(self.BASE_DIR, 'resources')
        self.RESOURCES_RAW_DIR = osp.join(self.RESOURCES_DIR, 'raw')
        self.RESOURCES_PROCESSED_DIR = osp.join(self.RESOURCES_DIR, 'processed')

        self.DROP_LABEL_VEHICLE = ['car_brand_model', 'vehicle_type_model','plate_number_definition','plate_representative_vehicle_image_name','parent_image_name','full_image_names','timestamp']
              

conf = Config()