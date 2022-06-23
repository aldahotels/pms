from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class PmsPartnerService(Component):
    _inherit = "base.rest.service"
    _name = "pms.partner.service"
    _usage = "partners"
    _collection = "pms.services"

    @restapi.method(
        [
            (
                [
                    "/",
                ],
                "GET",
            )
        ],
        output_param=Datamodel("pms.partner.info", is_list=True),
        auth="jwt_api_pms",
    )
    def get_partners(self):
        domain = []
        result_partners = []
        PmsPartnerInfo = self.env.datamodels["pms.partner.info"]
        for partner in self.env["res.partner"].search(
            domain,
        ):

            result_partners.append(
                PmsPartnerInfo(
                    id=partner.id,
                    name=partner.name,
                )
            )
        return result_partners

    @restapi.method(
        [
            (
                [
                    "/<string:documentType>/<string:documentNumber>",
                ],
                "GET",
            )
        ],
        output_param=Datamodel("pms.partner.info", is_list=True),
        auth="jwt_api_pms",
    )
    def get_partner_by_doc_number(self, document_type, document_number):
        doc_type = self.env["res.partner.id_category"].search(
            [("name", "=", document_type)]
        )
        doc_number = self.env["res.partner.id_number"].search(
            [("name", "=", document_number), ("category_id", "=", doc_type.id)]
        )
        partners = []
        PmsCheckinPartnerInfo = self.env.datamodels["pms.checkin.partner.info"]
        if not doc_number:
            pass
        else:
            if doc_number.valid_from:
                document_expedition_date = doc_number.valid_from.strftime("%d/%m/%Y")
            if doc_number.partner_id.birthdate_date:
                birthdate_date = doc_number.partner_id.birthdate_date.strftime(
                    "%d/%m/%Y"
                )
            partners.append(
                PmsCheckinPartnerInfo(
                    # id=doc_number.partner_id.id,
                    name=doc_number.partner_id.name
                    if doc_number.partner_id.name
                    else "",
                    firstname=doc_number.partner_id.firstname
                    if doc_number.partner_id.firstname
                    else "",
                    lastname=doc_number.partner_id.lastname
                    if doc_number.partner_id.lastname
                    else "",
                    lastname2=doc_number.partner_id.lastname2
                    if doc_number.partner_id.lastname2
                    else "",
                    email=doc_number.partner_id.email
                    if doc_number.partner_id.email
                    else "",
                    mobile=doc_number.partner_id.mobile
                    if doc_number.partner_id.mobile
                    else "",
                    documentType=doc_type.name,
                    documentNumber=doc_number.name,
                    documentExpeditionDate=document_expedition_date
                    if doc_number.valid_from
                    else "",
                    documentSupportNumber=doc_number.support_number
                    if doc_number.support_number
                    else "",
                    gender=doc_number.partner_id.gender
                    if doc_number.partner_id.gender
                    else "",
                    birthdate=birthdate_date
                    if doc_number.partner_id.birthdate_date
                    else "",
                    residenceStreet=doc_number.partner_id.residence_street
                    if doc_number.partner_id.residence_street
                    else "",
                    zip=doc_number.partner_id.residence_zip
                    if doc_number.partner_id.residence_zip
                    else "",
                    residenceCity=doc_number.partner_id.residence_city
                    if doc_number.partner_id.residence_city
                    else "",
                    nationality=doc_number.partner_id.nationality_id.name
                    if doc_number.partner_id.nationality_id
                    else "",
                    countryState=doc_number.partner_id.residence_state_id.name
                    if doc_number.partner_id.residence_state_id
                    else "",
                )
            )
        return partners
