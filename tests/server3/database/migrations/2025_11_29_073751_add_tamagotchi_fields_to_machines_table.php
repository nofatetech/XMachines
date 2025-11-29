<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('machines', function (Blueprint $table) {
            $table->integer('happiness')->default(50)->after('description');
            $table->integer('hunger')->default(0)->after('happiness');
            $table->boolean('is_auto_driving')->default(false)->after('fog_lights_on');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('machines', function (Blueprint $table) {
            $table->dropColumn(['happiness', 'hunger', 'is_auto_driving']);
        });
    }
};
