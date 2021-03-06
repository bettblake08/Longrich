""" This module hosts the main controller class """
import base64

from flask import jsonify, make_response, request

from app.database.models import (LongrichUserModel, PostModel, ProductModel,
                                 TagModel)


class MainController:
    @staticmethod
    def get_product(param):
        """ Get Product Endpoint
        :args
            param:  post id
        """
        try:
            post_id = int(param)

        except:
            return make_response(jsonify(
                {
                    "message": "Invalid product Id!"
                }
            ), 400
            )

        post = PostModel.find_by_id(post_id)

        if not post:
            return make_response(jsonify(
                {
                    "message": "Product does not exist!"
                }
            ), 404
            )

        product_data = {}

        product_data["log"] = post.json()
        post = post.get_post()
        post.get_stats()

        product_data["post"] = post.json()
        product_data["post"]["tags"] = post.get_tags()

        post.set_visitor(request.remote_addr)

        return make_response(jsonify(
            {
                "message": "You have successfully retrieved the product data!",
                "content": product_data
            }
        ), 200
        )

    @staticmethod
    def get_placement(name):
        """ Get Placement By Name Endpoint """
        users = LongrichUserModel.find_by_name(name)

        if not users:
            return make_response(jsonify(
                {
                    "message": "There are no users with the name {}!".format(name)
                }
            ), 404
            )

        return make_response(jsonify(
            {
                "message": "You have successfully retrieved the list of placements!",
                "content": [user.json() for user in users]
            }
        ), 200
        )

    @staticmethod
    def get_products(param):
        """ Get Products Endpoint
        :args
            offset  :   offset value used to paginate list of products
        """

        try:
            offset = int(param)

        except:
            return make_response(jsonify(
                {
                    "message": "Invalid offset!"
                }
            ), 400
            )

        posts = PostModel.get_posts_by_offset(offset)

        if not posts:
            return make_response(jsonify(
                {
                    "message": "There are no more products to list from given offset!"
                }
            ), 404
            )

        tags = []

        for post in posts:
            post = post.get_post()
            post_tags = post.tags

            for post_tag in post_tags:
                if post_tag.tagId not in tags:
                    tags.append(post_tag.tagId)

        tags_found = TagModel.get_all_tags(tags)
        content = []

        for post in posts:
            post_data = {}
            post = post.get_post()

            post_data["log"] = post.json()
            post_data["post"] = post.json()
            post_data["post"]["body"] = ""

            post_tags = post.tags
            post_tags_data = []

            for post_tag in post_tags:
                for tag_found in tags_found:
                    if post_tag.tagId == tag_found.id:
                        post_tags_data.append(tag_found.json())

            post_data["tags"] = post_tags_data
            content.append(post_data)

        return make_response(jsonify(
            {
                "message": "You have successfully retrieved all the products!",
                "content": content
            }
        ), 200
        )

    @staticmethod
    def product_reaction(param, param2):
        """ Set Reaction to Product Endpoint """

        try:
            product_reaction = int(param2)
            product_id = int(param)

        except:
            return make_response(jsonify(
                {
                    "message": "Invalid request!"
                }
            ), 400
            )

        if product_reaction not in [0, 1, 2]:
            return make_response(jsonify(
                {
                    "message": "Invalid reaction id!"
                }
            ), 400
            )

        product = ProductModel.find_by_id(product_id)

        if not product:
            return make_response(jsonify(
                {
                    "message": "Product does not exist!"
                }
            ), 404
            )
        try:
            product.set_reaction(request.remote_addr, product_reaction)
            return make_response(jsonify(
                {
                    "message": "You have successfully set a reaction to the product!"
                }
            ), 200
            )

        except:
            return make_response(jsonify(
                {
                    "message": "Failed to set the reaction to a product!"
                }
            ), 500
            )

    @staticmethod
    def get_form():
        """ Get Form Image Endpoint """
        form = open("../../../../resources/assets/images/form.png")
        encoded_form = None
        base64.encode(form, encoded_form)

        return {
            "message": "You have successfully retrieved the file!",
            "content": str(encoded_form)
        }
