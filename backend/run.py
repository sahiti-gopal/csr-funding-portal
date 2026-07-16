from app import create_app

app = create_app()

print("\n========== REGISTERED ROUTES ==========")

for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
    print(f"{rule.endpoint:35} {rule}")

print("=======================================\n")

if __name__ == "__main__":
    app.run(debug=True)