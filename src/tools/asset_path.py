import os

dirname = os.path.dirname(__file__)

def get_asset_path(asset_name):
	asset_path = os.path.join(dirname, "../assets", asset_name)

	if not os.path.exists(asset_path):
		raise FileNotFoundError(f"Asset '{asset_name}' not found in '{dirname}/../assets'")

	return asset_path