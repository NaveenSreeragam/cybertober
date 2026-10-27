import sys
from CTFd import create_app
from CTFd.utils import get_config, set_config
from CTFd.utils.config import get_themes, ctf_theme

app = create_app()

with app.app_context():
    print("Discovered themes:", get_themes())
    print("Previous theme:", get_config("ctf_theme"))
    
    # Activate haunted-network
    set_config("ctf_theme", "haunted-network")
    set_config("ctf_name", "The Haunted Network")
    print("New active theme:", get_config("ctf_theme"))
    
    # Test rendering routes using Flask test client
    client = app.test_client()
    routes_to_test = [
        ("/", "Landing Page"),
        ("/login", "Login Page"),
        ("/register", "Register Page"),
        ("/challenges", "Challenges Page"),
        ("/scoreboard", "Scoreboard Page"),
    ]
    
    all_ok = True
    for route, name in routes_to_test:
        resp = client.get(route, follow_redirects=True)
        html = resp.get_data(as_text=True)
        has_haunted = "THE HAUNTED NETWORK" in html or "haunted-network" in html
        print(f"Route '{route}' ({name}): Status {resp.status_code}, Contains theme tokens: {has_haunted}")
        if resp.status_code != 200:
            all_ok = False
            print(f"Error on route {route}")
            
    if all_ok:
        print("\nSUCCESS: All routes rendered successfully with 'haunted-network' active!")
    else:
        print("\nFAILURE: Some routes failed.")
        sys.exit(1)
