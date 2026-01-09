import json
import random
import time
import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "host": "localhost",
    "database": "marketplace",
    "user": "hones",
    "password": "secretpassword",
    "port": 9876
}

RECORD_COUNT = 100000
RANDOM_SEED = 91
MAX_RETRIES = 5
RETRY_DELAY = 2

def generate_product_data(num_records: int =10000) -> list[tuple]:
    """Generates synthetic product data with nested JSON metadata.

    Args:
        num_records (int, optional): Number of product records to generate. Defaults to 10000.

    Returns:
        list[tuple]: A list of tuples, each containing product data.
    """
    random.seed(RANDOM_SEED)
    
    categories = ["Electronics", "Appliances", "Apparel", "Furniture"]
    brands = ["HonesTech", "Lumina", "Apex", "EcoSmart", "Titan", "RoughEdge"]
    tags = ["new-arrival", "top-rated", "discounted", "eco-friendly"]
    
    data = []
    
    for i in range(num_records):
        category = random.choice(categories)
        brand = random.choice(brands)
        msrp = round(random.uniform(10.0, 1000.0), 2)
        
        metadata = {
            "pricing": {"msrp": msrp},
            "tags": random.sample(tags, 2),
            "specs": {
                "weight_kg": round(random.uniform(0.5, 50.0), 2)
            }
        }
        
        if category == "Electronics":
            metadata["specs"].update({
                "battery_life_hours": random.randint(1, 24),
                "wireless": random.choice([True, False])
                })
            metadata["sensors"] = [{
                "type": random.choice(["motion", "temperature", "humidity"]),
                "accuracy": random.choice(["high", "medium", "low"])
            }]
        elif category == "Furniture":
            metadata["dimensions_cm"] = {
                "length": round(random.uniform(50.0, 200.0), 2),
                "width": round(random.uniform(50.0, 200.0), 2),
                "height": round(random.uniform(50.0, 200.0), 2)
            }
            metadata["material"] = random.choice(["wood", "metal", "plastic", "composite"])
            metadata["assembly_required"] = random.choice([True, False])
        
        if random.random() > 0.8:
            metadata["pricing"]["sale_price"] = round(msrp * random.uniform(0.5, 0.9), 2)
        
        data.append((
            f"{brand} {category} Item {i+1}",
            category,
            brand,
            json.dumps(metadata)
        ))
    
    return data

def seed_database() -> None:
    """Seeds the PostgreSQL database with generated product data.
    """
    print("Connecting to the database...")
    
    connection = None
    
    print(f"Connecting to database at {DB_CONFIG['host']}...")
    
    # --- RETRY LOGIC FOR DOCKER STARTUP ---
    for attempt in range(MAX_RETRIES):
        try:
            connection = psycopg2.connect(**DB_CONFIG)
            break
        except psycopg2.OperationalError as e:
            if attempt == MAX_RETRIES - 1:
                print("Could not connect to the database after multiple attempts.")
                raise e
            print(f"Database starting up... retrying in {RETRY_DELAY}s (Attempt {attempt + 1}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
            
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 1. Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS products(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            brand TEXT,
            metadata JSONB
        )
        """
        cursor.execute(create_table_query)
        
        # 2. Clear existing data
        print("Clearing old data...")
        cursor.execute("TRUNCATE TABLE products RESTART IDENTITY")
        
        # 2a. Drop existing indexes
        print("Dropping existing indexes for a clean slate...")
        cursor.execute("DROP INDEX IF EXISTS idx_products_metadata;")
        
        # 3. Generate new data
        print(f"Generating {RECORD_COUNT} records...")
        records = generate_product_data(RECORD_COUNT)
        
        # 4. Insert new data
        print("Inserting records...")
        insert_query = """
        INSERT INTO products (name, category, brand, metadata)
        VALUES %s
        """
        execute_values(cursor, insert_query, records)
        
        connection.commit()
        cursor.close()
        
        print("Database seeding completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close() 


if __name__ == "__main__":
    seed_database()
            