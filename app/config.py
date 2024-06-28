from flask import Flask, request, session, make_response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from bbdd import *
from flask import jsonify
from historial_conversacion import *
from langchain_groq import ChatGroq
from nemoguardrails.llm.providers import register_llm_provider
from langchain_core.prompts import ChatPromptTemplate