import motor.motor_asyncio, datetime, pytz
from config import Config
import logging  # Added for logging errors and important information
from .utils import send_log


class Database:
    def __init__(self, uri, database_name):
        try:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            self._client.server_info()  # This will raise an exception if the connection fails
            logging.info("Successfully connected to MongoDB")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise e  # Re-raise the exception after logging it
        self.codeflixbots = self._client[database_name]
        self.col = self.codeflixbots.user

    def new_user(self, id):
        return dict(
            _id=int(id),
            join_date=datetime.date.today().isoformat(),
            file_id=None,
            caption=None,
            metadata=True,
            metadata_code="Telegram : @Codeflix_Bots",
            format_template=None,
            upload_as_document=False,  # New field for upload mode
            upload_destination=None,   # New field for upload destination
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            try:
                await self.col.insert_one(user)
                await send_log(b, u)
            except Exception as e:
                logging.error(f"Error adding user {u.id}: {e}")

    async def is_user_exist(self, id):
        try:
            user = await self.col.find_one({"_id": int(id)})
            return bool(user)
        except Exception as e:
            logging.error(f"Error checking if user {id} exists: {e}")
            return False

    async def total_users_count(self):
        try:
            count = await self.col.count_documents({})
            return count
        except Exception as e:
            logging.error(f"Error counting users: {e}")
            return 0

    async def get_all_users(self):
        try:
            all_users = self.col.find({})
            return all_users
        except Exception as e:
            logging.error(f"Error getting all users: {e}")
            return None

    async def delete_user(self, user_id):
        try:
            await self.col.delete_many({"_id": int(user_id)})
        except Exception as e:
            logging.error(f"Error deleting user {user_id}: {e}")

    async def set_thumbnail(self, id, file_id):
        try:
            await self.col.update_one({"_id": int(id)}, {"$set": {"file_id": file_id}})
        except Exception as e:
            logging.error(f"Error setting thumbnail for user {id}: {e}")

    async def get_thumbnail(self, id):
        try:
            user = await self.col.find_one({"_id": int(id)})
            return user.get("file_id", None) if user else None
        except Exception as e:
            logging.error(f"Error getting thumbnail for user {id}: {e}")
            return None

    async def set_caption(self, id, caption):
        try:
            await self.col.update_one({"_id": int(id)}, {"$set": {"caption": caption}})
        except Exception as e:
            logging.error(f"Error setting caption for user {id}: {e}")

    async def get_caption(self, id):
        try:
            user = await self.col.find_one({"_id": int(id)})
            return user.get("caption", None) if user else None
        except Exception as e:
            logging.error(f"Error getting caption for user {id}: {e}")
            return None

    async def set_format_template(self, id, format_template):
        try:
            await self.col.update_one(
                {"_id": int(id)}, {"$set": {"format_template": format_template}}
            )
        except Exception as e:
            logging.error(f"Error setting format template for user {id}: {e}")

    async def get_format_template(self, id):
        try:
            user = await self.col.find_one({"_id": int(id)})
            return user.get("format_template", None) if user else None
        except Exception as e:
            logging.error(f"Error getting format template for user {id}: {e}")
            return None

    async def set_media_preference(self, id, media_type):
        try:
            await self.col.update_one(
                {"_id": int(id)}, {"$set": {"media_type": media_type}}
            )
        except Exception as e:
            logging.error(f"Error setting media preference for user {id}: {e}")

    async def get_media_preference(self, id):
        try:
            user = await self.col.find_one({"_id": int(id)})
            return user.get("media_type", None) if user else None
        except Exception as e:
            logging.error(f"Error getting media preference for user {id}: {e}")
            return None

    async def get_metadata(self, user_id):
        user = await self.col.find_one({'_id': int(user_id)})
        return user.get('metadata', "Off")

    async def set_metadata(self, user_id, metadata):
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'metadata': metadata}})

    async def get_title(self, user_id):
        user = await self.col.find_one({'_id': int(user_id)})
        return user.get('title', 'Encoded by @Animes_Cruise')

    async def set_title(self, user_id, title):
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'title': title}})

    async def get_author(self, user_id):
        user = await self.col.find_one({'_id': int(user_id)})
        return user.get('author', '@Animes_Cruise')

    async def set_author(self, user_id, author):
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'author': author}})

    async def get_artist(self, user_id):
        user = await self.col.find_one({'_id': int(user_id)})
        return user.get('artist', '@Animes_Cruise')

    async def set_artist(self, user_id, artist):
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'artist': artist}})

    async def get_audio(self, user_id):
        user = await self.col.find_one({'_id': int(user_id)})
        return user.get('audio', '@Animes_Cruise')

    async def set_audio(self, user_id, audio):
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'audio': audio}})

    async def get_subtitle(self, user_id):
        user = await self.col.find_one({'_id': int(user_id)})
        return user.get('subtitle', '@Animes_Cruise')

    async def set_subtitle(self, user_id, subtitle):
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'subtitle': subtitle}})

    async def get_video(self, user_id):
        user = await self.col.find_one({'_id': int(user_id)})
        return user.get('video', '@Animes_Cruise')

    async def set_video(self, user_id, video):
        await self.col.update_one({'_id': int(user_id)}, {'$set': {'video': video}})

    # New methods for settings functionality

    async def get_upload_mode(self, user_id):
        """Get user's upload mode preference (True = document, False = media)"""
        try:
            user = await self.col.find_one({"_id": int(user_id)})
            return user.get("upload_as_document", False) if user else False
        except Exception as e:
            logging.error(f"Error getting upload mode for user {user_id}: {e}")
            return False

    async def set_upload_mode(self, user_id, upload_as_document):
        """Set user's upload mode preference"""
        try:
            await self.col.update_one(
                {"_id": int(user_id)}, 
                {"$set": {"upload_as_document": upload_as_document}}
            )
        except Exception as e:
            logging.error(f"Error setting upload mode for user {user_id}: {e}")

    async def get_upload_destination(self, user_id):
        """Get user's upload destination info"""
        try:
            user = await self.col.find_one({"_id": int(user_id)})
            return user.get("upload_destination", None) if user else None
        except Exception as e:
            logging.error(f"Error getting upload destination for user {user_id}: {e}")
            return None

    async def set_upload_destination(self, user_id, destination_data):
        """Set user's upload destination"""
        try:
            await self.col.update_one(
                {"_id": int(user_id)}, 
                {"$set": {"upload_destination": destination_data}}
            )
        except Exception as e:
            logging.error(f"Error setting upload destination for user {user_id}: {e}")

    async def remove_upload_destination(self, user_id):
        """Remove user's upload destination (reset to private chat)"""
        try:
            await self.col.update_one(
                {"_id": int(user_id)}, 
                {"$set": {"upload_destination": None}}
            )
        except Exception as e:
            logging.error(f"Error removing upload destination for user {user_id}: {e}")

    # Ban status methods
    async def is_banned(self, id):
        try:
            user = await self.col.find_one({"_id": int(id)})
            if user:
                ban_status = user.get("ban_status", {})
                return ban_status.get("is_banned", False)
            return False
        except Exception as e:
            logging.error(f"Error checking ban status for user {id}: {e}")
            return False

    async def ban_user(self, user_id, ban_duration, ban_reason):
        try:
            ban_time = datetime.datetime.now()
            ban_status = dict(
                is_banned=True,
                ban_duration=ban_duration,
                banned_on=ban_time.isoformat(),
                ban_reason=ban_reason
            )
            await self.col.update_one(
                {"_id": int(user_id)}, 
                {"$set": {"ban_status": ban_status}}
            )
        except Exception as e:
            logging.error(f"Error banning user {user_id}: {e}")

    async def unban_user(self, user_id):
        try:
            ban_status = dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
            await self.col.update_one(
                {"_id": int(user_id)}, 
                {"$set": {"ban_status": ban_status}}
            )
        except Exception as e:
            logging.error(f"Error unbanning user {user_id}: {e}")

    async def get_ban_status(self, user_id):
        try:
            user = await self.col.find_one({"_id": int(user_id)})
            if user:
                return user.get("ban_status", {})
            return {}
        except Exception as e:
            logging.error(f"Error getting ban status for user {user_id}: {e}")
            return {}

    # Additional utility methods
    async def get_user_settings(self, user_id):
        """Get all user settings in one call"""
        try:
            user = await self.col.find_one({"_id": int(user_id)})
            if user:
                return {
                    'upload_as_document': user.get('upload_as_document', False),
                    'upload_destination': user.get('upload_destination', None),
                    'format_template': user.get('format_template', None),
                    'caption': user.get('caption', None),
                    'file_id': user.get('file_id', None),
                    'metadata': user.get('metadata', 'Off'),
                    'media_type': user.get('media_type', None)
                }
            return {}
        except Exception as e:
            logging.error(f"Error getting user settings for user {user_id}: {e}")
            return {}

    async def update_user_settings(self, user_id, settings_dict):
        """Update multiple user settings at once"""
        try:
            await self.col.update_one(
                {"_id": int(user_id)}, 
                {"$set": settings_dict}
            )
        except Exception as e:
            logging.error(f"Error updating user settings for user {user_id}: {e}")


# Create the database instance
codeflixbots = Database(Config.DB_URL, Config.DB_NAME)
