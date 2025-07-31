import frappe


def after_install():
    customize_language_dt()
    sync_languages()

    frappe.db.commit()


def customize_language_dt():
    custom_fields = [
        {
            "label": "Language Name (English)",
            "fieldname": "custom_language_name_en",
            "fieldtype": "Data",
            "insert_after": "language_name",
        }
    ]

    for property_setter in custom_fields:
        if not frappe.db.exists(
            "Custom Field",
            {"dt": "Language", "fieldname": property_setter["fieldname"]},
        ):
            new_property_setter = frappe.get_doc(
                {
                    "doctype": "Custom Field",
                    "dt": "Language",
                    "module": "Geo Addons",
                    **property_setter,
                }
            )
            new_property_setter.insert()

    property_setters = [
        {
            "doctype_or_field": "DocType",
            "doc_type": "Language",
            "property": "title_field",
            "property_type": "Data",
            "value": "custom_language_name_en",
        }
    ]
    for property_setter in property_setters:
        if not frappe.db.exists(
            "Property Setter",
            {
                "doc_type": "Language",
                "property": property_setter["property"],
                "value": property_setter["value"],
            },
        ):
            new_property_setter = frappe.get_doc(
                {
                    "doctype": "Property Setter",
                    "module": "Geo Addons",
                    **property_setter,
                }
            )
            new_property_setter.insert()


def sync_languages():
    """Sync crm_geo_addons/languages.json with Language"""
    with open(frappe.get_app_path("crm_geo_addons", "languages.json")) as f:
        data = frappe.json.loads(f.read())

    for language in data:
        if frappe.db.exists("Language", language["code"]):
            frappe.db.set_value(
                "Language",
                language["code"],
                "custom_language_name_en",
                language["english_name"],
            )
