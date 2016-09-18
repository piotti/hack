from django.http import JsonResponse


def test(request):
	return JsonResponse(
	{
		'nearby_players':
			[

				{
					'A':1,
					'B':'one',
					'C':True

				},
				{
					'A':2,
					'B':'two',
					'C':False

				},
				{
					'A':3,
					'B':'three',
					'C':True

				}

			]

	}

	)
