from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatConversation, ChatMessage
from .services import ResearchAssistantService
from .serializers import ChatConversationSerializer, ChatMessageSerializer

@login_required
def assistant_view(request):
    """Interactive research chat interface."""
    conversations = request.user.chat_conversations.prefetch_related('messages').order_by('-updated_at')
    active_conversation = conversations.first()

    return render(request, 'assistant/assistant.html', {
        'conversations': conversations,
        'active_conversation': active_conversation,
    })


# ---------------- REST API ENDPOINTS ----------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_chat(request):
    """Send user message and receive grounded research response."""
    message = request.data.get('message', '').strip()
    conv_id = request.data.get('conversation_id')

    if not message:
        return Response({'error': 'Message content cannot be blank'}, status=400)

    result = ResearchAssistantService.process_query(
        user=request.user,
        message_text=message,
        conversation_id=conv_id
    )
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_conversations(request):
    """List recent research conversations."""
    conversations = request.user.chat_conversations.all()[:15]
    serializer = ChatConversationSerializer(conversations, many=True)
    return Response({'results': serializer.data})
