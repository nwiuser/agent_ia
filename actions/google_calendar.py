"""
Module Google Calendar - Gestion des événements
"""
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class GoogleCalendarManager:
    """Gestionnaire pour Google Calendar API"""
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.service = None
        
        if not demo_mode:
            self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Calendar API service"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            creds = None
            
            token_file = os.getenv("GOOGLE_CALENDAR_TOKEN_FILE", "token.pickle")
            credentials_file = os.getenv("GOOGLE_CALENDAR_CREDENTIALS_FILE", "credentials.json")
            
            # Load existing credentials
            if os.path.exists(token_file):
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # Get new credentials if needed
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(credentials_file):
                        logger.error(f"Credentials file not found: {credentials_file}")
                        logger.info("Falling back to demo mode")
                        self.demo_mode = True
                        return
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                
                # Save credentials
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('calendar', 'v3', credentials=creds)
            logger.info("Google Calendar service initialized")
            
        except Exception as e:
            logger.error(f"Error initializing Google Calendar: {e}")
            logger.info("Falling back to demo mode")
            self.demo_mode = True
    
    async def create_event(
        self,
        title: str,
        date: str,
        time: str,
        duration_minutes: int = 60,
        description: Optional[str] = None,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crée un événement dans Google Calendar
        
        Args:
            title: Titre de l'événement
            date: Date au format YYYY-MM-DD
            time: Heure au format HH:MM
            duration_minutes: Durée en minutes
            description: Description optionnelle
            location: Lieu optionnel
            
        Returns:
            Dict avec le statut et les détails
        """
        if self.demo_mode:
            return self._mock_create_event(title, date, time, duration_minutes, description, location)
        
        try:
            # Parse date and time
            start_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            end_datetime = start_datetime + timedelta(minutes=duration_minutes)
            
            event = {
                'summary': title,
                'description': description or '',
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'Europe/Paris',
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'Europe/Paris',
                },
            }
            
            if location:
                event['location'] = location
            
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            logger.info(f"Event created: {created_event.get('htmlLink')}")
            
            return {
                "status": "success",
                "message": f"Événement '{title}' créé avec succès",
                "event_id": created_event.get('id'),
                "event_link": created_event.get('htmlLink'),
                "start": start_datetime.isoformat(),
                "end": end_datetime.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating event: {e}")
            return {
                "status": "error",
                "message": f"Erreur lors de la création de l'événement: {str(e)}"
            }
    
    def _mock_create_event(
        self,
        title: str,
        date: str,
        time: str,
        duration_minutes: int,
        description: Optional[str],
        location: Optional[str]
    ) -> Dict[str, Any]:
        """Version mock pour la démonstration"""
        logger.info(f"[MOCK] Creating event: {title} on {date} at {time}")
        
        start_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        
        return {
            "status": "mock",
            "message": f"✅ [DEMO] Événement '{title}' créé dans Google Calendar",
            "event_id": f"mock_event_{datetime.now().timestamp()}",
            "event_link": "https://calendar.google.com/calendar/",
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat(),
            "details": {
                "title": title,
                "date": date,
                "time": time,
                "duration_minutes": duration_minutes,
                "description": description,
                "location": location
            }
        }
    
    async def update_event(self, event_id: str, **kwargs) -> Dict[str, Any]:
        """Met à jour un événement existant"""
        if self.demo_mode:
            return {
                "status": "mock",
                "message": f"✅ [DEMO] Événement {event_id} mis à jour"
            }
        
        try:
            event = self.service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            # Update fields
            for key, value in kwargs.items():
                if key in event:
                    event[key] = value
            
            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            return {
                "status": "success",
                "message": "Événement mis à jour",
                "event_link": updated_event.get('htmlLink')
            }
            
        except Exception as e:
            logger.error(f"Error updating event: {e}")
            return {
                "status": "error",
                "message": f"Erreur: {str(e)}"
            }
    
    async def delete_event(self, event_id: str) -> Dict[str, Any]:
        """Supprime un événement"""
        if self.demo_mode:
            return {
                "status": "mock",
                "message": f"✅ [DEMO] Événement {event_id} supprimé"
            }
        
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            return {
                "status": "success",
                "message": "Événement supprimé"
            }
            
        except Exception as e:
            logger.error(f"Error deleting event: {e}")
            return {
                "status": "error",
                "message": f"Erreur: {str(e)}"
            }


# Instance globale
_calendar_manager = None


def get_calendar_manager(demo_mode: bool = None) -> GoogleCalendarManager:
    """Récupère ou crée l'instance du gestionnaire Calendar"""
    global _calendar_manager
    
    if demo_mode is None:
        demo_mode = os.getenv("DEMO_MODE", "True").lower() == "true"
    
    if _calendar_manager is None:
        _calendar_manager = GoogleCalendarManager(demo_mode=demo_mode)
    
    return _calendar_manager
