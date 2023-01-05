#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 5 2023
@author: MohammadHossein Salari

This code generate a What a Year Tintin and Captain Haddock meme and sends it to Mastodon

inspired by:
            - https://mastodon.lol/@codefiscal/109630875913117948
            - https://sigmoid.social/@whataweekhuh@hostux.social
            - https://twitter.com/tintinades/status/1610305758146560003?s=20&t=-UIljrxbnLRR-_JPtNJlxg
"""

import os
from mastodon import Mastodon
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont


def set_up_mastodon():
    """
    Sets up a Mastodon API client.

    Returns:
        Mastodon: A Mastodon API client.
    """

    load_dotenv()
    access_token = os.environ["MASTODON_ACCESS_TOKEN"]

    # Create a Mastodon API client using the provided access token
    mastodon = Mastodon(
        access_token=access_token,
        api_base_url="https://sigmoid.social/",
    )

    # Return the Mastodon API client
    return mastodon


def generate_the_meme(base_path):
    """
    This function takes in a base path and generates a meme image using the base path to find
    the necessary images and fonts.The generated image is then returned.

    Inputs:
        base_path: string containing the base path for finding the necessary images and fonts

    Returns:
        out: an Image object containing the generated meme
    """

    # Construct the file paths for the input image and font
    input_image_path = os.path.join(base_path, "images", "what a year, huh.png")
    font_path = os.path.join(base_path, "fonts", "Tintin_Dialogue.ttf")

    # Open the base image and convert it to RGBA
    with Image.open(input_image_path).convert("RGBA") as base:

        # Create a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

        # Draw the "what a year, huh? ..." on the image
        fnt = ImageFont.truetype(font_path, 90)
        d = ImageDraw.Draw(txt)
        d.text((150, 170), "what a year, huh? ...", font=fnt, fill=(0, 0, 0, 255))

        # Get the the current date and draw "Captain, its __today__!" on the image
        fnt = ImageFont.truetype(font_path, 55)
        d.text(
            (120, 375),
            f"Captain, its {datetime.now().strftime('%B %-d')}!",
            font=fnt,
            fill=(0, 0, 0, 255),
        )

        # Combine the text with the base image
        out = Image.alpha_composite(base, txt)
    return out


if __name__ == "__main__":

    # Find the path of this code folder on the hard drive
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Generate and save the meme
    image = generate_the_meme(base_path)
    output_image_path = os.path.join(base_path, "images", "out.png")
    image.save(output_image_path)

    # Connect to Mastodon API
    mastodon_api = set_up_mastodon()

    # Send the image to Mastodon
    media_id = mastodon_api.media_post(output_image_path)

    # Remove the image from hard drive
    os.remove(output_image_path)

    # send the toot to Mastodon
    mastodon_api.status_post("#whatayearhuh", media_ids=media_id)
