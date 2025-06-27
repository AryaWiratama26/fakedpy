from faker import Faker
import pandas as pd
import json
from pathlib import Path
from typing import Union, Literal

class FakedGenerator:
    def __init__(self, locale: Union[str, list] = 'en_US'):
        """
        Initialize the FakedGenerator
        
        Parameters:
        locale: str or list - Locale for fake data generation (e.g., 'id_ID' for Indonesian)
        """
        self.fake = Faker(locale)
        
    def _get_fake_dict(self):
        return {
            # Personal Information
            "name": self.fake.name,
            "first_name": self.fake.first_name,
            "last_name": self.fake.last_name,
            "email": self.fake.email,
            "phone_number": self.fake.phone_number,
            "date": self.fake.date,
            "gender": lambda: self.fake.random_element(elements=('Male', 'Female')),
            
            # Address Information
            "address": self.fake.address,
            "street_address": self.fake.street_address,
            "city": self.fake.city,
            "state": self.fake.state,
            "country": self.fake.country,
            "postcode": self.fake.postcode,
            "latitude": self.fake.latitude,
            "longitude": self.fake.longitude,
            
            # Internet Information
            "username": self.fake.user_name,
            "password": self.fake.password,
            "domain_name": self.fake.domain_name,
            "url": self.fake.url,
            "ipv4": self.fake.ipv4,
            "ipv6": self.fake.ipv6,
            "mac_address": self.fake.mac_address,
            
            # Company Information
            "company": self.fake.company,
            "job": self.fake.job,
            
            # Financial Information
            "credit_card_number": self.fake.credit_card_number,
            "credit_card_provider": self.fake.credit_card_provider,
            "currency_code": self.fake.currency_code,
            
            # Technology
            "file_name": self.fake.file_name,
            "file_extension": self.fake.file_extension,
            "mime_type": self.fake.mime_type,
            
            # Miscellaneous
            "text": self.fake.text,
            "word": self.fake.word,
            "sentence": self.fake.sentence,
            "paragraph": self.fake.paragraph,
            "color_name": self.fake.color_name,
            "hex_color": self.fake.hex_color,
            "rgb_color": self.fake.rgb_color,
        }

    def generate(
        self,
        rows: int = 10,
        fields: list = ["name", "address", "job"],
        output_format: Literal["csv", "json", "excel", "parquet"] = "csv",
        output_path: Union[str, Path] = "output",
        related_fields: dict = None
    ) -> pd.DataFrame:
        """
        Generate fake data and save to specified format
        
        Parameters:
        -----------
        rows : int
            Number of rows to generate
        fields : list
            List of fields to include in output
        output_format : str
            Format to save the data ('csv', 'json', 'excel', or 'parquet')
        output_path : str or Path
            Path where to save the output file (without extension)
        related_fields : dict
            Dictionary of related fields, e.g., {"user_id": {"type": "counter", "start": 1}}
            or {"department": {"type": "choice", "values": ["IT", "HR", "Finance"]}}
        
        Returns:
        --------
        pd.DataFrame
            Generated fake data
        """
        fake_dict = self._get_fake_dict()
        data = []
        
        # Handle related fields
        if related_fields:
            for field, config in related_fields.items():
                if config["type"] == "counter":
                    start = config.get("start", 1)
                    fake_dict[field] = lambda i=iter(range(start, rows + start)): next(i)
                elif config["type"] == "choice":
                    values = config["values"]
                    fake_dict[field] = lambda v=values: self.fake.random_element(elements=v)
        
        # Generate data
        for i in range(rows):
            content = {col: fake_dict[col]() if callable(fake_dict.get(col)) else None 
                      for col in fields if col in fake_dict or col in (related_fields or {})}
            data.append(content)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to specified format
        output_path = Path(output_path)
        if output_format == "csv":
            df.to_csv(f"{output_path}.csv", index=False)
        elif output_format == "json":
            df.to_json(f"{output_path}.json", orient="records", indent=2)
        elif output_format == "excel":
            df.to_excel(f"{output_path}.xlsx", index=False)
        elif output_format == "parquet":
            df.to_parquet(f"{output_path}.parquet", index=False)
            
        return df

def faked(rows: int = 10, req: list = ["name", "address", "job"]) -> pd.DataFrame:
    """Legacy function for backward compatibility"""
    generator = FakedGenerator()
    return generator.generate(rows=rows, fields=req)

