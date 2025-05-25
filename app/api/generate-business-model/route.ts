import { NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(request: Request) {
  try {
    const { prompt } = await request.json();

    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "You are a helpful assistant that generates business model ideas." },
        { role: "user", content: prompt }
      ],
    });

    const businessModel = completion.choices[0].message.content;

    return NextResponse.json({ businessModel });
  } catch (error) {
    console.error('Error in generate-business-model API:', error);
    return NextResponse.json({ error: 'Failed to generate business model' }, { status: 500 });
  }
}