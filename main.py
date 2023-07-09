import os
from rent import main as rent_main
from snimu import main as snimu_main
from job import main as job_main
from sell import main as sell_main
from services import main as services_main

def main():
    if not os.path.exists("result"):
        os.mkdir("result")
        
    rent_main()
    snimu_main()
    job_main()
    sell_main()
    services_main()

if __name__ == '__main__':
    main()
