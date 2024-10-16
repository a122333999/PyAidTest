{
	"type": "group",
	"iden": "3c4d7163-5ce2-4dbc-b953-3c3e72b5aa72",
	"name": "测试TransmitPage",
	"desc": "测试TransmitPage的测试组",
	
	"cases": [
		{
			"type": "case",
			"iden": "3c425f31-344f-4383-bf52-d20828f8a043",
			"name": "创建ETH报文1",
			"desc": "创建一个ETH报文的测试用例",

			"start": "741ee909-d55c-45b5-8516-20ed160479cc",
			"active": true,
			"actions": [
				{
					"type": "check",
					"iden": "741ee909-d55c-45b5-8516-20ed160479cc",
					"name": "打开菜单",
					"desc": ".......",
					
					"class": "images",
					"delay": 1000,
					"times": 0,
					"retry": 0,
					"child": "9a0fff5c-3d29-4eba-acae-29f2bf4b52c3",
					"config": {
						"rect": {"top": null, "left":  null, "right": null, "bottom": null},
						"offset": {"top": 0, "left":  0, "right": 0, "bottom": 0},
						"source": "shot:none|last:none|uuid:UUID",
						"targets": ["file:图片1", "file:图片2"],

						"duration": 1000,
						"count": 5,
						"hit": 2
					}
				},
				{
					"type": "operate",
					"iden": "9a0fff5c-3d29-4eba-acae-29f2bf4b52c3",
					"name": "点击菜单",
					"desc": ".......",
					
					"class": "click",
					"delay": 1000,
					"times": 0,
					"retry": 0,
					"child": "0fe433e2-f488-465c-aa06-9411e0490a3a",
					"config": {
						"point": "last:center",
						"offset": {"x": 0, "y": 0},

						"time": -1,
						"keys": ["Ctrl", "A"],
						"roll": 10,
						"content": "user:AAABBB"
					}
				},
				{
					"type": "control",
					"iden": "0fe433e2-f488-465c-aa06-9411e0490a3a",
					"name": "如果找到目标",
					"desc": ".......",

					"class": "fork",
					"delay": 1000,
					"times": 0,
					"retry": 0,
					"child": "7749684f-7ddf-4d8f-85c1-614d890c5165",
					"config": {
						"fork": {"goto": null, "eval": "last:default"}
					}
				},
				{
					"type": "empty",
					"iden": "7749684f-7ddf-4d8f-85c1-614d890c5165",
					"name": "空节点",
					"desc": "空白节点",

					"class": "empty",
					"delay": 1000,
					"times": 0,
					"retry": 0,
					"child": null,
					"config": {}
				}
			]
		}
	]
}